# Template Assets Integration Guide

## 📁 Copy Kusina Template Files

The Django project is ready, but you need to copy the template assets (CSS, JS, images, fonts) from the Kusina template folder.

### Files to Copy

**Source Folder**: `f:\sunshine\kusina-master\`  
**Target Folder**: `f:\sunshine\sip-sunshine-django\static\`

### Step-by-Step Instructions

#### Windows (Command Prompt or PowerShell):

```batch
REM Navigate to the Django project
cd f:\sunshine\sip-sunshine-django

REM Copy CSS files
xcopy f:\sunshine\kusina-master\css\* static\css\ /Y /E

REM Copy JavaScript files
xcopy f:\sunshine\kusina-master\js\* static\js\ /Y /E

REM Copy Images
xcopy f:\sunshine\kusina-master\images\* static\images\ /Y /E

REM Copy Fonts
xcopy f:\sunshine\kusina-master\fonts\* static\fonts\ /Y /E
```

#### macOS/Linux (Terminal):

```bash
# Navigate to Django project
cd /path/to/sip-sunshine-django

# Copy CSS files
cp -r /path/to/kusina-master/css/* static/css/

# Copy JavaScript files
cp -r /path/to/kusina-master/js/* static/js/

# Copy Images
cp -r /path/to/kusina-master/images/* static/images/

# Copy Fonts
cp -r /path/to/kusina-master/fonts/* static/fonts/
```

### File Structure After Copying

```
static/
├── css/
│   ├── animate.css
│   ├── aos.css
│   ├── bootstrap-datepicker.css
│   ├── bootstrap.min.css
│   ├── flaticon.css
│   ├── icomoon.css
│   ├── ionicons.min.css
│   ├── jquery.timepicker.css
│   ├── magnific-popup.css
│   ├── open-iconic-bootstrap.min.css
│   ├── owl.carousel.min.css
│   ├── owl.theme.default.min.css
│   ├── style.css
│   └── bootstrap/
│       └── ... (bootstrap files)
│
├── js/
│   ├── aos.js
│   ├── bootstrap-datepicker.js
│   ├── bootstrap.min.js
│   ├── google-map.js
│   ├── jquery-3.2.1.min.js
│   ├── jquery-migrate-3.0.1.min.js
│   ├── jquery.animateNumber.min.js
│   ├── jquery.easing.1.3.js
│   ├── jquery.magnific-popup.min.js
│   ├── jquery.min.js
│   ├── jquery.stellar.min.js
│   ├── jquery.timepicker.min.js
│   ├── jquery.waypoints.min.js
│   ├── main.js
│   ├── owl.carousel.min.js
│   ├── popper.min.js
│   ├── range.js
│   └── scrollax.min.js
│
├── images/
│   ├── (all kusina template images)
│
└── fonts/
    ├── flaticon/
    ├── icomoon/
    ├── ionicons/
    └── open-iconic/
```

## ✅ Verification Checklist

After copying files, verify:

- [ ] `static/css/style.css` exists
- [ ] `static/css/bootstrap.min.css` exists
- [ ] `static/js/jquery.min.js` exists
- [ ] `static/js/main.js` exists
- [ ] `static/images/` folder has images
- [ ] `static/fonts/` folder has fonts
- [ ] All CSS files present
- [ ] All JS files present

## 🔍 Test CSS/JS Loading

1. Run the Django server:
   ```bash
   python manage.py runserver
   ```

2. Visit: `http://localhost:8000/`

3. Right-click → "Inspect" or "View Page Source"

4. Look for in `<head>` section:
   ```html
   <link rel="stylesheet" href="/static/css/bootstrap.min.css">
   <link rel="stylesheet" href="/static/css/style.css">
   ```

5. Scroll to bottom, look for:
   ```html
   <script src="/static/js/jquery.min.js"></script>
   <script src="/static/js/main.js"></script>
   ```

6. Check browser console (F12) for errors:
   - Should show 0 404 errors for static files
   - Should load without errors

## 🎨 CSS/JS Files Used in Templates

The following files are referenced in `templates/base.html`:

**CSS:**
- bootstrap.min.css
- animate.css
- icomoon.css
- ionicons.min.css
- bootstrap-datepicker.css
- jquery.timepicker.css
- owl.carousel.min.css
- owl.theme.default.min.css
- magnific-popup.css
- aos.css
- flaticon.css
- style.css (main styles)

**JavaScript:**
- jquery.min.js
- jquery-migrate-3.0.1.min.js
- popper.min.js
- bootstrap.min.js
- bootstrap-datepicker.js
- jquery.timepicker.min.js
- owl.carousel.min.js
- jquery.magnific-popup.min.js
- aos.js
- jquery.waypoints.min.js
- jquery.animateNumber.min.js
- scrollax.min.js
- main.js (custom scripts)

## 🐛 If Assets Don't Load

### Issue: 404 errors for static files

**Check:**
```bash
# Verify files exist
dir static\css\style.css
dir static\js\main.js
dir static\images\
```

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput
```

**Or restart server:**
```bash
# Stop: Ctrl+C
# Run again:
python manage.py runserver
```

### Issue: Styles not applied

1. Hard refresh browser: `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)
2. Clear browser cache
3. Check browser console for 404 errors
4. Verify file paths in `templates/base.html`

### Issue: JavaScript not working

1. Check browser console (F12) for JS errors
2. Verify jQuery loaded before other scripts
3. Check main.js has no syntax errors
4. Try hard refresh

## 📝 Important Notes

- **Don't move files** - Keep Django file structure as-is
- **File permissions** - Ensure files are readable
- **Path style** - Windows uses `\`, Django uses `/` in templates
- **Case sensitivity** - Use lowercase for static file references
- **Development server** - Django serves static files automatically
- **Production** - Will need to run `collectstatic` command

## ✨ After Copying Assets

1. Restart Django server: `python manage.py runserver`
2. Visit homepage: `http://localhost:8000/`
3. Check if CSS/JS loaded (should see styled navbar, formatted content)
4. Open browser developer tools (F12)
5. Look at Network tab - all static files should load (200 status)
6. Look at Console tab - should have no errors

## 🎁 What Happens After Copy

Once assets are copied:
- ✅ Website will be styled (no more plain text)
- ✅ Navbar will be formatted
- ✅ Colors and fonts will appear
- ✅ Animations will work
- ✅ Images will load
- ✅ Forms will be styled
- ✅ Footer will be formatted
- ✅ Everything will look professional

---

**This is the final step to get your website fully functional!**

After copying assets:
1. Restart Django server
2. Open `http://localhost:8000/`
3. Your restaurant website should be fully styled and functional!

Enjoy! 🚀
