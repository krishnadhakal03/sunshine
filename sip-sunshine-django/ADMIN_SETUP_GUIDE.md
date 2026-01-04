# Admin Setup Guide - Contact & Reservation Pages

## Overview
The Contact and Reservation pages require certain settings to be configured in the Django admin. This guide will help you set them up properly.

---

## 1. Access Django Admin

1. Navigate to: `http://localhost:2005/admin/`
2. Login with your credentials:
   - Username: `admin`
   - Password: `admin123456`

---

## 2. Configure Site Settings

### Why This is Important
- The Contact page displays your restaurant's **address**, **phone**, and **email**
- The Contact page can embed a **Google Map** 
- Both pages use this data for contact information cards

### Steps to Configure:

1. **In Admin Dashboard**, look for **"Site Settings"** under the **Restaurant** section
2. Click on it to open the Site Setting configuration
3. Fill in the following fields:

#### **Basic Information**
- **Site Name**: `Sip and SunShine` (or your restaurant name)
- **Site Description**: Brief description of your restaurant
- **Site Keywords**: SEO keywords separated by commas
- **Site Logo**: Upload your logo image (optional)
- **Site Favicon**: Upload your favicon image (optional)

#### **Contact Information** (Required for Contact Page)
- **Email**: Your contact email (e.g., `info@sipandsunshine.com`)
- **Phone**: Your phone number (e.g., `+31 (0)6 12345678`)
- **Address**: Your full address (e.g., `123 Restaurant Street, Amsterdam, Netherlands`)

#### **Social Media** (Optional)
- **Facebook URL**: Link to your Facebook page
- **Instagram URL**: Link to your Instagram profile
- **Twitter URL**: Link to your Twitter profile

#### **Location** (Required for Map on Contact Page)
- **Google Map Embed**: Paste the embed code from Google Maps
  
  **How to get Google Map Embed Code:**
  1. Go to [Google Maps](https://maps.google.com)
  2. Search for your restaurant location
  3. Click the **Share** button
  4. Select the **Embed a map** tab
  5. Copy the entire `<iframe>` code
  6. Paste it in the **Google Map Embed** field

   **Example:**
   ```html
   <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2435.1234567!2d4.8952!3d52.3702!" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
   ```

4. Click **Save** at the bottom of the page

---

## 3. What Happens After Setup

### Contact Page
- **Address Card**: Shows your configured address
- **Phone Card**: Shows clickable phone link
- **Email Card**: Shows clickable email link
- **Google Map Section**: Shows embedded map (if configured) or helpful placeholder

### Reservation Page
- Uses the same settings for display
- Form collects guest reservations

### Fallback Behavior
If any of these settings are not configured:
- **Address**: Shows `123 Restaurant Street, Amsterdam, Netherlands`
- **Phone**: Shows `+31 (0)6 12345678`
- **Email**: Shows `info@sipandsunshine.com`
- **Map**: Shows a helpful message indicating map is not configured

---

## 4. Troubleshooting

### "Contact Information cards are empty"
- **Solution**: Go to Admin > Site Settings and fill in the email, phone, and address fields

### "Map section shows placeholder message"
- **Solution**: 
  1. Get your Google Map embed code (see instructions above)
  2. Paste it in the **Google Map Embed** field in Site Settings
  3. Save changes

### "Can't find Site Settings in Admin"
- **Reason**: Only one Site Settings record can exist in the system
- **Solution**: 
  1. Click on **"Site Settings"** in the Restaurant section
  2. If it shows a list, click on the existing setting to edit it
  3. If it says "Add Site Setting" is not allowed, it means the setting exists - click to view and edit it

---

## 5. Production Checklist

Before going live, make sure:
- ✅ Site Name is set correctly
- ✅ Contact Email is valid and monitored
- ✅ Phone number is correct
- ✅ Address is complete and accurate
- ✅ Google Map embed code is pasted correctly
- ✅ Social media URLs point to your actual accounts (optional but recommended)
- ✅ Logo and Favicon are uploaded (optional but improves branding)

---

## 6. Quick Reference

| Page | Displays | Requires |
|------|----------|----------|
| Contact | Form, Info Cards, Map | Email, Phone, Address, Map Embed Code |
| Reservation | Form, Hours | None (standalone) |
| All Pages | Footer with Contact Info | Email, Phone, Address, Logo |

---

## 7. Testing

After configuration:

1. **Visit Contact Page**: `http://localhost:2005/contact/`
   - Check if address, phone, email are displayed
   - Check if map appears correctly (or placeholder if not configured)

2. **Visit Reservation Page**: `http://localhost:2005/reservation/`
   - Verify form displays correctly
   - Test form submission

3. **Check Footer**: On any page
   - Verify your contact details appear in footer
   - Verify logo displays correctly

---

## Need Help?

If you encounter issues:
1. Ensure you're logged into the admin with proper credentials
2. Verify the Site Settings record exists (there should be only one)
3. Check browser console for any JavaScript errors
4. Refresh the page after making admin changes

