# Zaviyar Collections — Clothing Store

A fresh clothing-store project, separate from the existing appliances project. Built with Streamlit and designed with a clean white, soft-pink and elegant floral theme.

## Included
- Separate 2 Piece, 3 Piece and Ready-Made catalogs
- Animated/interactive styling, responsive layout, search and product details
- Add to bag, quantity changes and checkout details
- WhatsApp order message with customer details, item names, quantities and total
- Admin login, product add/edit/delete, multiple uploaded images, prices, stock and sold-out status
- `LIMITED STOCK` badge when 1–3 items remain; exact stock is only shown in Admin
- Store WhatsApp number and announcement-bar settings

## Important setup
1. Create a new GitHub repository for this project.
2. Upload `app.py`, `requirements.txt`, and this README.
3. On Streamlit Community Cloud, create a new app using this repository, branch `main`, main file `app.py`.
4. In Streamlit app Settings → Secrets, set:
   ```toml
   ADMIN_USERNAME = "choose-your-admin-username"
   ADMIN_PASSWORD = "choose-a-long-unique-password"
   STORE_BRAND = "Zaviyar Collections"
   ```
5. Open the app, log in from Admin, and set the WhatsApp order number using country code and digits only, e.g. `923001234567`.

## Data persistence warning
This starter saves store data and uploaded images to local files. On some hosted environments, local files can be reset when the app restarts or redeploys. For a real production shop, connect a persistent database and image storage (for example Supabase) before relying on it for live inventory or customer orders.

## WhatsApp checkout
Checkout opens WhatsApp with a prefilled order. The customer must tap **Send**. Fully automatic delivery requires a WhatsApp Business Platform integration.
