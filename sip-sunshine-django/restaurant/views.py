from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http import JsonResponse, Http404
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.utils import OperationalError, ProgrammingError
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from .models import (
    Page, MenuItem, ContentBlock, BlogPost, 
    Reservation, ContactMessage, SiteSetting, Order, OrderItem, CustomerProfile
)
from .checkout_views import CheckoutView, OrderConfirmationView, OrderTrackingView, CreateOrderView


class PageView(TemplateView):
    """Display any page by template name"""
    
    def get_template_names(self):
        slug = self.kwargs.get('slug', 'home')
        page = get_object_or_404(Page, slug=slug, is_active=True)
        
        # Map template names
        template_map = {
            'index': 'pages/index.html',
            'about': 'pages/about.html',
            'menu': 'pages/menu.html',
            'blog': 'pages/blog.html',
            'contact': 'pages/contact.html',
            'reservation': 'pages/reservation.html',
        }
        return [template_map.get(page.template_name, 'pages/page.html')]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug', 'home')
        page = get_object_or_404(Page, slug=slug, is_active=True)
        
        context['page'] = page
        context['content_blocks'] = ContentBlock.objects.filter(is_active=True)
        
        return context


class HomePageView(TemplateView):
    """Home page view"""
    template_name = 'pages/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = get_object_or_404(Page, slug='home', is_active=True)
        context['content_blocks'] = ContentBlock.objects.filter(is_active=True)
        context['menu_items'] = MenuItem.objects.filter(is_active=True)[:6]
        context['featured_menu_items'] = MenuItem.objects.filter(is_active=True)[:6]
        # Get published blog posts
        blog_posts = BlogPost.objects.filter(is_published=True)[:3]
        # Filter to only include posts with valid slugs (this happens in the template too)
        context['blog_posts'] = [post for post in blog_posts if post.slug]
        return context


class MenuPageView(TemplateView):
    """Menu page with categorized items"""
    template_name = 'pages/menu.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Do not hard-fail if CMS pages haven't been seeded yet (tests/first-run).
        context['page'] = Page.objects.filter(slug='menu', is_active=True).first()

        # Get all active menu items
        menu_items = MenuItem.objects.filter(is_active=True).order_by('category', 'order', 'id')
        context['menu_items'] = menu_items

        # Provide the variables expected by the existing template.
        # Anything not matching known categories is treated as main courses.
        known = {key for key, _label in getattr(MenuItem, 'CATEGORY_CHOICES', [])}
        context['appetizers'] = menu_items.filter(category__in=['appetizers', 'Appetizers'])
        context['desserts'] = menu_items.filter(category__in=['desserts', 'Desserts'])
        context['beverages'] = menu_items.filter(category__in=['beverages', 'Beverages', 'drinks', 'Drinks'])
        main_known = menu_items.filter(category__in=['main_courses', 'main', 'Main', 'Side', 'main courses', 'Main Courses'])
        fallback = menu_items.exclude(category__in=list(known))
        context['main_courses'] = (main_known | fallback).distinct()

        # Keep older grouping structure too (used elsewhere)
        categories = {}
        for item in menu_items:
            category = item.get_category_display() if hasattr(item, 'get_category_display') else (item.category or '')
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        context['categories'] = categories
        context['featured_items'] = menu_items[:6]
        
        return context


class BlogListView(ListView):
    """Blog listing page"""
    model = BlogPost
    template_name = 'pages/blog.html'
    context_object_name = 'blog_posts'
    paginate_by = 9
    
    def get_queryset(self):
        # Get all published blog posts
        return BlogPost.objects.filter(is_published=True).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = get_object_or_404(Page, slug='blog', is_active=True)
        return context


class BlogDetailView(DetailView):
    """Blog post detail page"""
    model = BlogPost
    template_name = 'pages/blog-single.html'
    context_object_name = 'post'
    slug_field = 'translations__slug'
    
    def get_queryset(self):
        # Get published blog posts
        return BlogPost.objects.filter(is_published=True)
    
    def get_object(self, queryset=None):
        """Override to get slug from translated field in current language"""
        if queryset is None:
            queryset = self.get_queryset()
        
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is not None:
            # Get the blog post by matching the slug in the current language
            queryset = queryset.filter(translations__slug=slug)
        
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['related_posts'] = BlogPost.objects.filter(
            is_published=True
        ).exclude(id=post.id)[:3]
        return context


class AboutPageView(TemplateView):
    """About page view"""
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = get_object_or_404(Page, slug='about', is_active=True)
        context['content_blocks'] = ContentBlock.objects.filter(
            block_type='about',
            is_active=True
        )
        return context


class ReservationView(TemplateView):
    """Reservation page"""
    template_name = 'pages/reservation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = get_object_or_404(Page, slug='reservation', is_active=True)
        try:
            context['site_settings'] = SiteSetting.objects.first()
        except:
            pass
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle reservation form submission"""
        try:
            reservation = Reservation.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                reservation_date=request.POST.get('reservation_date'),
                reservation_time=request.POST.get('reservation_time'),
                number_of_guests=request.POST.get('number_of_guests'),
                special_requests=request.POST.get('special_requests', ''),
            )
            messages.success(request, 'Reservation request submitted successfully!')
            return redirect('reservation')
        except Exception as e:
            messages.error(request, 'Error submitting reservation. Please try again.')
            return redirect('reservation')


class ContactView(TemplateView):
    """Contact page"""
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = get_object_or_404(Page, slug='contact', is_active=True)
        try:
            context['site_settings'] = SiteSetting.objects.first()
        except:
            pass
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle contact form submission"""
        try:
            ContactMessage.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone', ''),
                subject=request.POST.get('subject'),
                message=request.POST.get('message'),
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        except Exception as e:
            messages.error(request, 'Error sending message. Please try again.')
            return redirect('contact')


class CreateOrderView(View):
    """Handle order creation from menu page"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        """Create a new order"""
        try:
            guest_name = request.POST.get('guest_name', '').strip()
            item_name = request.POST.get('item_name', '').strip()
            item_price = request.POST.get('item_price', 0)
            quantity = int(request.POST.get('quantity', 1))
            order_type = request.POST.get('order_type', 'seated')
            special_instructions = request.POST.get('special_instructions', '').strip()
            
            # Validation
            if not guest_name or not item_name:
                return JsonResponse({
                    'success': False,
                    'message': 'Guest name and item name are required'
                })
            
            # Create order
            order = Order.objects.create(
                guest_name=guest_name,
                order_type=order_type,
                special_requests=special_instructions,
                total_price=0
            )
            
            # Add order details based on type
            if order_type == 'seated':
                table_number = request.POST.get('table_number', '')
                if table_number:
                    try:
                        order.table_number = int(table_number)
                    except (ValueError, TypeError):
                        pass
                    order.save()
            else:  # online
                guest_email = request.POST.get('guest_email', '').strip()
                guest_phone = request.POST.get('guest_phone', '').strip()
                delivery_address = request.POST.get('delivery_address', '').strip()
                delivery_city = request.POST.get('delivery_city', '').strip()
                delivery_postal_code = request.POST.get('delivery_postal_code', '').strip()
                delivery_country = request.POST.get('delivery_country', '').strip()
                
                if guest_email:
                    order.guest_email = guest_email
                if guest_phone:
                    order.guest_phone = guest_phone
                if delivery_address:
                    order.delivery_address = delivery_address
                if delivery_city:
                    order.delivery_city = delivery_city
                if delivery_postal_code:
                    order.delivery_postal_code = delivery_postal_code
                if delivery_country:
                    order.delivery_country = delivery_country
                
                order.save()
            
            # Create order item
            subtotal = float(item_price) * quantity
            order_item = OrderItem.objects.create(
                order=order,
                item_name=item_name,
                item_price=float(item_price),
                quantity=quantity,
                special_instructions=special_instructions
            )
            
            # Update order total
            order.total_price = subtotal
            order.save()
            
            return JsonResponse({
                'success': True,
                'order_id': order.id,
                'message': f'Order created successfully'
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })


# ==================== Customer Authentication Views ====================

class CustomerRegisterView(View):
    """Customer registration for valued customers"""
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('menu')
        return render(request, 'auth/register.html', {
            'page_title': 'Register - Sip and Sunshine'
        })
    
    def post(self, request):
        email = request.POST.get('email', '').strip().lower()
        first_name = request.POST.get('first_name', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        # Validation
        errors = {}
        
        if not email or not first_name or not password:
            errors['general'] = 'All fields are required'
        
        if password != password_confirm:
            errors['password'] = 'Passwords do not match'
        
        if len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters'
        
        if User.objects.filter(email=email).exists():
            errors['email'] = 'This email is already registered'
        
        if errors:
            return render(request, 'auth/register.html', {
                'errors': errors,
                'form_data': request.POST
            }, status=400)
        
        # Create user
        try:
            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                first_name=first_name,
                password=password
            )

            # Profile is optional if DB migrations haven't been applied yet.
            try:
                CustomerProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'phone': phone,
                    },
                )
            except (OperationalError, ProgrammingError):
                # Example: "no such table: restaurant_customerprofile" on fresh DB.
                pass
            
            # Auto-login after registration
            login(request, user)
            messages.success(request, f'Welcome, {first_name}! Your account has been created.')
            return redirect('restaurant:menu')
        
        except Exception as e:
            errors['general'] = f'Registration failed: {str(e)}'
            return render(request, 'auth/register.html', {
                'errors': errors,
                'form_data': request.POST
            }, status=400)


class CustomerLoginView(View):
    """Customer login for valued customers"""
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('restaurant:menu')
        return render(request, 'auth/login.html', {
            'page_title': 'Login - Sip and Sunshine'
        })
    
    def post(self, request):
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '').strip()
        
        if not email or not password:
            return render(request, 'auth/login.html', {
                'errors': {'general': 'Email and password are required'}
            }, status=400)
        
        # Authenticate using email (username in this case)
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('restaurant:menu')
        else:
            return render(request, 'auth/login.html', {
                'errors': {'general': 'Invalid email or password'},
                'form_data': {'email': email}
            }, status=400)


class CustomerLogoutView(View):
    """Customer logout"""
    
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
        return redirect('restaurant:menu')


class CustomerProfileView(View):
    """View customer profile and order history"""
    
    @method_decorator(login_required(login_url='restaurant:customer_login'))
    def get(self, request):
        user = request.user
        try:
            profile, _ = CustomerProfile.objects.get_or_create(user=user)
        except (OperationalError, ProgrammingError):
            profile = None
        orders = Order.objects.filter(
            guest_email=user.email
        ).order_by('-created_at')

        active_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'out_for_delivery']
        current_order = orders.filter(status__in=active_statuses).first()
        estimated_time = None
        if current_order and getattr(current_order, 'estimated_completion_time', None):
            try:
                estimated_time = current_order.estimated_completion_time.strftime('%H:%M')
            except Exception:
                estimated_time = None
        
        return render(request, 'auth/profile.html', {
            'user': user,
            'profile': profile,
            'current_order': current_order,
            'current_order_estimated_time': estimated_time,
            'orders': orders,
            'page_title': 'My Profile - Sip and Sunshine'
        })

    @method_decorator(login_required(login_url='restaurant:customer_login'))
    def post(self, request):
        user = request.user
        try:
            profile, _ = CustomerProfile.objects.get_or_create(user=user)
        except (OperationalError, ProgrammingError):
            messages.warning(request, 'Profile storage is not available yet. Please ask an admin to run database migrations.')
            return redirect('restaurant:customer_profile')

        # Basic profile fields
        first_name = (request.POST.get('first_name') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        preferred_payment_method = (request.POST.get('preferred_payment_method') or '').strip()

        # Default delivery address
        delivery_address = (request.POST.get('delivery_address') or '').strip()
        delivery_city = (request.POST.get('delivery_city') or '').strip()
        delivery_postal_code = (request.POST.get('delivery_postal_code') or '').strip()
        delivery_country = (request.POST.get('delivery_country') or '').strip()

        if first_name:
            user.first_name = first_name
            user.save(update_fields=['first_name'])

        profile.phone = phone
        profile.delivery_address = delivery_address
        profile.delivery_city = delivery_city
        profile.delivery_postal_code = delivery_postal_code
        if delivery_country:
            profile.delivery_country = delivery_country

        if preferred_payment_method in {'cash', 'stripe', 'paypal'}:
            profile.preferred_payment_method = preferred_payment_method

        profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('restaurant:customer_profile')


class OrderConfirmationView(View):
    """Order confirmation and tracking page"""
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_items = order.items.all()
        
        return render(request, 'orders/confirmation.html', {
            'order': order,
            'order_items': order_items,
            'page_title': 'Order Confirmation - Sip and Sunshine'
        })


class OrderTrackingView(View):
    """Track order status"""
    
    def get(self, request):
        if request.GET.get('order_id'):
            order_id = request.GET.get('order_id')
            try:
                order = Order.objects.get(id=order_id)
                return render(request, 'orders/tracking.html', {
                    'order': order,
                    'order_items': order.items.all(),
                    'page_title': 'Track Your Order - Sip and Sunshine'
                })
            except Order.DoesNotExist:
                return render(request, 'orders/tracking.html', {
                    'error': 'Order not found',
                    'page_title': 'Track Your Order - Sip and Sunshine'
                }, status=404)
        
        return render(request, 'orders/tracking.html', {
            'page_title': 'Track Your Order - Sip and Sunshine'
        })

