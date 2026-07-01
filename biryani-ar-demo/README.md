# Biryani AR Menu Demo

## Why the QR may show a wrong page
The QR inside this demo currently points to a placeholder URL:

`https://your-domain.com/biryani-ar-demo/`

That is not your real hosted website. If you scan it before hosting, the phone can open a domain-parking/ad page.

## How to make the QR work
1. Upload this full folder to hosting, for example Netlify, Vercel, Hostinger, GoDaddy, or your client's server.
2. Get the final live URL, for example:
   `https://restaurant-name.netlify.app/`
3. Regenerate the QR code for that final URL.
4. Replace `assets/biryani-ar-qr.png` and update the embedded QR inside `index.html`.

## Important camera note
For camera AR on mobile, the page should be opened from HTTPS. Camera may not work from normal HTTP links.

## Files
- `index.html` — main AR menu demo
- `assets/biryani-photo.jpg` — uploaded biryani image
- `assets/biryani-ar-qr.png` — placeholder QR image
