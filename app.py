import os, json, html, urllib.parse, hashlib, hmac
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu

APP_DIR = Path(__file__).parent
DATA_FILE = APP_DIR / "store_data.json"
UPLOAD_DIR = APP_DIR / "product_images"
UPLOAD_DIR.mkdir(exist_ok=True)
BRAND = os.getenv("STORE_BRAND", "ZAVIYAR COLLECTIONS")
DEFAULT_DATA = {
    "whatsapp": "",
    "admin_username": "",
    "admin_password_hash": "",
    "announcement": "NEW SEASON ❀ NEW STORIES ❀ DISCOVER YOUR STYLE",
    "products": [
        {"id": 1, "name": "Ivory Bloom 3 Piece", "category": "3 Piece", "price": 5490, "old_price": 6490, "stock": 3, "sold": False, "description": "An elegant three-piece look with delicate details.", "images": [], "sizes": ["Unstitched"]},
        {"id": 2, "name": "Sage Grace 2 Piece", "category": "2 Piece", "price": 3890, "old_price": 0, "stock": 8, "sold": False, "description": "A fresh everyday look, made for effortless styling.", "images": [], "sizes": ["Unstitched"]},
        {"id": 3, "name": "Ready-to-Wear Edit", "category": "Ready-Made", "price": 0, "old_price": 0, "stock": 0, "sold": False, "description": "Your ready-made collection will appear here soon.", "images": [], "sizes": ["S", "M", "L", "XL"]},
    ],
    "next_id": 4
}
def load_data():
    if DATA_FILE.exists():
        try:
            d=json.loads(DATA_FILE.read_text(encoding="utf-8"))
            d.setdefault("whatsapp",""); d.setdefault("admin_username",""); d.setdefault("admin_password_hash",""); d.setdefault("announcement",DEFAULT_DATA["announcement"])
            d.setdefault("products",[]); d.setdefault("next_id",max([p.get("id",0) for p in d["products"]]+[0])+1)
            return d
        except Exception: pass
    return json.loads(json.dumps(DEFAULT_DATA))
def save_data(d):
    DATA_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
def money(n): return "Rs. " + format(int(n or 0), ",")
def img_src(path):
    return path if path and (str(path).startswith("http://") or str(path).startswith("https://")) else None

st.set_page_config(page_title=f"{BRAND} | Clothing", page_icon="✦", layout="wide", initial_sidebar_state="collapsed")
data=load_data()
if "cart" not in st.session_state: st.session_state.cart={}
if "admin" not in st.session_state: st.session_state.admin=False
if "page" not in st.session_state: st.session_state.page="Home"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root { --ink:#20201e; --muted:#77756f; --line:#ece9e3; --cream:#f8f7f3; --accent:#c9869b; --pink:#f7e8ed; --rose:#b76e86; }
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
/* Explicit high-contrast form styling: labels must never be white on white */
.stApp, .stApp p, .stApp label, .stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stWidgetLabel"] p, .stApp [data-testid="stWidgetLabel"] label {
  color:#292522 !important;
}
.stApp input, .stApp textarea, .stApp [data-baseweb="select"] > div {
  background:#ffffff !important; color:#24211f !important;
  -webkit-text-fill-color:#24211f !important; border:1px solid #d9cbd0 !important;
}
.stApp input::placeholder, .stApp textarea::placeholder {
  color:#77716f !important; -webkit-text-fill-color:#77716f !important; opacity:1 !important;
}
.stApp [data-testid="stForm"] {background:#fffafb!important;}
.stApp [data-testid="stAlert"] p {color:inherit!important;}

.stApp {background:#fff;color:var(--ink);}
.block-container {max-width:1380px;padding-top:1rem;padding-bottom:3rem;}
#MainMenu, footer, header {visibility:hidden;}
.brand {font-family:'Playfair Display',serif;font-size:2.1rem;letter-spacing:.19em;font-weight:600;text-align:center;color:#222;margin:.15rem 0 .3rem;}
.eyebrow {text-align:center;font-size:.68rem;letter-spacing:.27em;color:#b4778d;text-transform:uppercase;}
.announcement {background:#222;color:#fff;text-align:center;padding:10px 8px;letter-spacing:.15em;font-size:.69rem;margin:1rem 0 1.5rem;}
.hero {background:linear-gradient(120deg,#fff7fa 0%,#fff 48%,#f6e4eb 100%);border:1px solid #f1dfe6;padding:4rem 2.3rem;border-radius:3px;position:relative;overflow:hidden;}
.hero h1 {font-family:'Playfair Display',serif;font-size:clamp(2.3rem,5vw,4.5rem);line-height:1.04;font-weight:500;max-width:760px;margin:0 0 1rem;}
.hero p {color:#6f6a63;max-width:510px;font-size:1rem;line-height:1.8;}
.pill {display:inline-block;border:1px solid #dfb7c5;padding:7px 13px;border-radius:100px;font-size:.68rem;letter-spacing:.15em;text-transform:uppercase;color:#a65f79;margin-bottom:1.2rem;}
.section-title {font-family:'Playfair Display',serif;font-size:2rem;margin:2.4rem 0 .3rem;}
.section-sub {color:#817d76;font-size:.86rem;margin-bottom:1.2rem;}
.product-card {border:1px solid #efede8;background:#fff;padding:10px;transition:transform .25s ease,box-shadow .25s ease;border-radius:3px;height:100%;}
.product-card:hover {transform:translateY(-5px);box-shadow:0 14px 35px rgba(30,25,20,.08);}
.product-image {height:245px;background:linear-gradient(135deg,#fff2f6,#f0dce4);display:flex;align-items:center;justify-content:center;color:#bd8b9d;font-size:2.5rem;overflow:hidden;}
.product-image img {width:100%;height:100%;object-fit:cover;}
.product-name {font-family:'Playfair Display',serif;font-size:1.12rem;margin:.8rem 0 .2rem;}
.product-meta {color:#8a857d;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;}
.price {font-weight:600;font-size:.95rem;margin-top:.5rem;}
.old-price {text-decoration:line-through;color:#aaa;font-size:.8rem;margin-left:8px;font-weight:400;}
.stock {display:inline-block;background:#fbeaf0;color:#9c5b75;padding:5px 8px;font-size:.66rem;letter-spacing:.08em;margin-top:.55rem;}
.sold {background:#242321;color:#fff;}
hr {border-color:#eeece7!important;}
div.stButton>button {border-radius:2px;border:1px solid #252523;background:#252523;color:white;min-height:2.7rem;letter-spacing:.06em;transition:all .2s;}
div.stButton>button:hover {background:#b76e86;border-color:#b76e86;color:#fff;transform:translateY(-1px);}
div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stNumberInput"] input, div[data-testid="stSelectbox"] div {border-radius:2px!important;}
.footer {background:#fff5f8;padding:2rem;text-align:center;color:#777;font-size:.78rem;margin-top:3rem;letter-spacing:.05em;}
.small-label {font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:#ad7087;}
div[data-testid="stMetric"] {background:#fff5f8;padding:1rem;border:1px solid #eee9e1;}
</style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="brand">{html.escape(BRAND)}</div><div class="eyebrow">❀ A considered wardrobe · Made for your moments ❀</div>', unsafe_allow_html=True)
st.markdown(f'<div class="announcement">{html.escape(data.get("announcement",""))}</div>', unsafe_allow_html=True)

# top navigation
navcols=st.columns([1,1,1,1,1,1])
navs=["Home","2 Piece","3 Piece","Ready-Made","My Cart","Admin"]
for col, n in zip(navcols,navs):
    with col:
        if st.button(("✦ " if n=="Home" else "")+n, key="nav_"+n, use_container_width=True):
            st.session_state.page=n
            st.rerun()
st.divider()

page=st.session_state.page
if page=="Admin":
    st.markdown('<div class="section-title">Admin Studio</div><div class="section-sub">Private store management</div>',unsafe_allow_html=True)
    # First-run credential setup lives in the app. Password is stored as a hash, not plain text.
    if not data.get("admin_password_hash"):
        st.info("First-time setup: create your private admin username and password.")
        with st.form("first_admin_setup"):
            new_user=st.text_input("Create admin username",placeholder="Choose a username")
            new_pass=st.text_input("Create admin password",type="password",placeholder="Use at least 10 characters")
            confirm_pass=st.text_input("Confirm admin password",type="password")
            setup=st.form_submit_button("Create admin login",use_container_width=True)
        if setup:
            if len(new_user.strip())<4: st.error("Username must be at least 4 characters.")
            elif len(new_pass)<10: st.error("Password must be at least 10 characters.")
            elif new_pass!=confirm_pass: st.error("Passwords do not match.")
            else:
                data["admin_username"]=new_user.strip()
                data["admin_password_hash"]=hashlib.sha256(new_pass.encode("utf-8")).hexdigest()
                save_data(data)
                st.session_state.admin=True
                st.success("Admin login created. You are signed in.")
                st.rerun()
        st.caption("Note: this starter stores settings in the app's local data file. For a public live shop, connect persistent database storage before relying on it.")
        st.stop()

    if not st.session_state.admin:
        with st.form("admin_login"):
            st.write("Sign in to manage products, stock and order contact settings.")
            username=st.text_input("Admin username",placeholder="Enter admin username")
            password=st.text_input("Admin password", type="password",placeholder="Enter admin password")
            submitted=st.form_submit_button("Sign in securely", use_container_width=True)
        if submitted:
            expected_user=data.get("admin_username","")
            expected_hash=data.get("admin_password_hash","")
            given_hash=hashlib.sha256(password.encode("utf-8")).hexdigest()
            if expected_user and expected_hash and username.strip()==expected_user and hmac.compare_digest(given_hash,expected_hash):
                st.session_state.admin=True; st.success("Signed in."); st.rerun()
            else:
                st.error("Username or password is incorrect. Check capitalization and try again.")
        st.stop()
    st.success("Admin session active")
    if st.button("Log out"):
        st.session_state.admin=False; st.rerun()
    tab1,tab2,tab3,tab4=st.tabs(["Products & stock","Add product","Store settings","Admin login"])
    with tab1:
        products=data["products"]
        if not products: st.info("No products yet. Add your first product.")
        for p in products:
            with st.expander(f'#{p["id"]} · {p["name"]} · Stock: {p["stock"]}'):
                with st.form(f'edit_{p["id"]}'):
                    c1,c2=st.columns(2)
                    name=c1.text_input("Product name",p.get("name",""))
                    category=c2.selectbox("Catalog",["2 Piece","3 Piece","Ready-Made"],index=["2 Piece","3 Piece","Ready-Made"].index(p.get("category","2 Piece")) if p.get("category") in ["2 Piece","3 Piece","Ready-Made"] else 0)
                    price=c1.number_input("Current price (PKR)",min_value=0,value=int(p.get("price",0)),step=100)
                    old=c2.number_input("Original price (optional)",min_value=0,value=int(p.get("old_price",0)),step=100)
                    stock=c1.number_input("Available stock (private)",min_value=0,value=int(p.get("stock",0)),step=1)
                    sold=c2.checkbox("Mark as SOLD / unavailable",value=bool(p.get("sold",False)))
                    desc=st.text_area("Description",p.get("description",""))
                    urls=st.text_area("Image URLs (one per line; upload images on Add product for new photos)", "\n".join(p.get("images",[])))
                    save=st.form_submit_button("Save changes",use_container_width=True)
                if save:
                    p.update({"name":name.strip(),"category":category,"price":int(price),"old_price":int(old),"stock":int(stock),"sold":bool(sold),"description":desc.strip(),"images":[x.strip() for x in urls.splitlines() if x.strip()]})
                    save_data(data); st.success("Product updated."); st.rerun()
                if st.button("Delete this product",key=f'del_{p["id"]}'):
                    data["products"]=[x for x in data["products"] if x["id"]!=p["id"]]
                    save_data(data); st.rerun()
    with tab2:
        with st.form("new_product",clear_on_submit=True):
            name=st.text_input("Product name")
            category=st.selectbox("Catalog",["2 Piece","3 Piece","Ready-Made"])
            c1,c2=st.columns(2)
            price=c1.number_input("Price (PKR)",min_value=0,step=100)
            old=c2.number_input("Original price (optional)",min_value=0,step=100)
            stock=st.number_input("Available stock",min_value=0,step=1)
            desc=st.text_area("Description")
            photos=st.file_uploader("Upload multiple product photos",type=["png","jpg","jpeg","webp"],accept_multiple_files=True)
            urls=st.text_area("Or paste image URLs (one per line)")
            submit=st.form_submit_button("Add product",use_container_width=True)
        if submit:
            if not name.strip(): st.error("Please enter a product name.")
            else:
                images=[x.strip() for x in urls.splitlines() if x.strip()]
                for i, photo in enumerate(photos or []):
                    safe="".join(ch for ch in photo.name if ch.isalnum() or ch in "._-")
                    target=UPLOAD_DIR/f'{data["next_id"]}_{i}_{safe}'
                    target.write_bytes(photo.getbuffer()); images.append(str(target.relative_to(APP_DIR)))
                data["products"].append({"id":data["next_id"],"name":name.strip(),"category":category,"price":int(price),"old_price":int(old),"stock":int(stock),"sold":False,"description":desc.strip(),"images":images,"sizes":["Unstitched"] if category!="Ready-Made" else ["S","M","L","XL"]})
                data["next_id"]+=1; save_data(data); st.success("Product added."); st.rerun()
    with tab3:
        with st.form("store_settings"):
            wa=st.text_input("WhatsApp number for orders (country code, digits only)",value=data.get("whatsapp",""),placeholder="923001234567")
            announcement=st.text_input("Announcement bar",value=data.get("announcement",""))
            submitted=st.form_submit_button("Save store settings",use_container_width=True)
        if submitted:
            data["whatsapp"]="".join(ch for ch in wa if ch.isdigit())
            data["announcement"]=announcement.strip()
            save_data(data); st.success("Settings saved.")
        st.caption("Keep the WhatsApp number in international format without +, spaces or dashes.")
    with tab4:
        st.write("Change your admin login here.")
        with st.form("change_admin_login"):
            new_user=st.text_input("New admin username",value=data.get("admin_username",""))
            current_pass=st.text_input("Current password",type="password")
            new_pass=st.text_input("New password",type="password")
            confirm_pass=st.text_input("Confirm new password",type="password")
            change=st.form_submit_button("Update admin login",use_container_width=True)
        if change:
            current_hash=hashlib.sha256(current_pass.encode("utf-8")).hexdigest()
            if not hmac.compare_digest(current_hash,data.get("admin_password_hash","")):
                st.error("Current password is incorrect.")
            elif len(new_user.strip())<4:
                st.error("Username must be at least 4 characters.")
            elif len(new_pass)<10:
                st.error("New password must be at least 10 characters.")
            elif new_pass!=confirm_pass:
                st.error("New passwords do not match.")
            else:
                data["admin_username"]=new_user.strip()
                data["admin_password_hash"]=hashlib.sha256(new_pass.encode("utf-8")).hexdigest()
                save_data(data); st.success("Admin login updated.")
    st.stop()

# storefront
if page=="Home":
    st.markdown("""
    <div class="hero">
      <div class="pill">The new season edit</div>
      <h1>Wear what<br>feels like <i>you.</i></h1>
      <p>Thoughtfully selected looks, beautiful details and timeless pieces for your everyday moments and special occasions.</p>
    </div>
    """,unsafe_allow_html=True)
    st.markdown('<div class="section-title">Find your kind of style</div><div class="section-sub">Explore our collections</div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    for col,title,desc in [(c1,"02 / TWO PIECE","Easy, effortless everyday looks"),(c2,"03 / THREE PIECE","Complete looks for every occasion"),(c3,"04 / READY-MADE","Ready-to-wear · Coming soon")]:
        with col:
            st.markdown(f'<div style="background:#fff5f8;padding:1.5rem;min-height:130px;border:1px solid #efebe4"><div class="small-label">{title}</div><h3 style="font-family:Playfair Display,serif;font-weight:500">{desc}</h3></div>',unsafe_allow_html=True)
            target={"02 / TWO PIECE":"2 Piece","03 / THREE PIECE":"3 Piece","04 / READY-MADE":"Ready-Made"}[title]
            if st.button("Explore collection →",key="explore_"+target,use_container_width=True): st.session_state.page=target; st.rerun()
    display=[p for p in data["products"] if not (p.get("category")=="Ready-Made" and not p.get("price"))]
    st.markdown('<div class="section-title">The latest edit</div><div class="section-sub">Pieces we think you’ll love</div>',unsafe_allow_html=True)
else:
    category=page if page in ["2 Piece","3 Piece","Ready-Made"] else None
    st.markdown(f'<div class="section-title">{html.escape(page)}</div><div class="section-sub">Discover the collection</div>',unsafe_allow_html=True)
    display=[p for p in data["products"] if p.get("category")==category]

if page=="My Cart":
    st.markdown('<div class="section-title">Your shopping bag</div>',unsafe_allow_html=True)
    cart=st.session_state.cart
    products_by_id={str(p["id"]):p for p in data["products"]}
    total=0
    if not cart: st.info("Your bag is waiting for something beautiful.")
    else:
        for pid,qty in list(cart.items()):
            p=products_by_id.get(str(pid))
            if not p: continue
            c1,c2,c3=st.columns([4,1,1])
            c1.write(f'**{p["name"]}**  \n{money(p["price"])} each')
            newqty=c2.number_input("Qty",min_value=1,max_value=max(1,int(p.get("stock",1))),value=min(int(qty),max(1,int(p.get("stock",1)))),key=f"qty_{pid}")
            st.session_state.cart[pid]=int(newqty)
            c3.write(money(p["price"]*int(newqty)))
            total+=p["price"]*int(newqty)
            if st.button("Remove",key=f"remove_{pid}"): del st.session_state.cart[pid]; st.rerun()
        st.divider()
        st.subheader(f"Total: {money(total)}")
        st.markdown("### Delivery details")
        with st.form("checkout"):
            customer=st.text_input("Full name *")
            phone=st.text_input("Phone number *")
            address=st.text_area("Complete delivery address *")
            city=st.text_input("City *")
            notes=st.text_area("Order notes (optional)")
            submit=st.form_submit_button("Continue to WhatsApp order",use_container_width=True)
        if submit:
            if not all([customer.strip(),phone.strip(),address.strip(),city.strip()]): st.error("Please complete all required delivery details.")
            elif not data.get("whatsapp"): st.error("The store owner has not configured the WhatsApp order number yet.")
            else:
                lines=["NEW CLOTHING ORDER",f"Name: {customer}",f"Phone: {phone}",f"Address: {address}",f"City: {city}","", "ITEMS:"]
                for pid,qty in cart.items():
                    p=products_by_id.get(str(pid))
                    if p:
                        if p.get("sold") or int(p.get("stock",0))<int(qty):
                            st.error(f'{p["name"]} is no longer available in the requested quantity. Please update your bag.')
                            st.stop()
                        lines.append(f'{p["name"]} x {qty} — {money(p["price"]*int(qty))}')
                lines += ["",f"Total: {money(total)}",f"Notes: {notes or 'None'}","Please confirm availability and delivery."]
                wa_url="https://wa.me/"+data["whatsapp"]+"?text="+urllib.parse.quote("\n".join(lines))
                st.markdown(f'[Tap here to send your order on WhatsApp]({wa_url})')
                st.info("WhatsApp will open with the order message ready. Tap Send to deliver it to the store.")
    st.stop()

# product cards
if not display:
    st.info("No products in this collection yet. New styles will appear here soon.")
else:
    search=st.text_input("⌕  Search this collection",placeholder="Search by product name...")
    if search: display=[p for p in display if search.lower() in p.get("name","").lower()]
    cols=st.columns(3)
    for i,p in enumerate(display):
        with cols[i%3]:
            images=p.get("images",[])
            local_image=None
            for im in images:
                if img_src(im): local_image=im; break
                if im and (APP_DIR/im).exists(): local_image=str(APP_DIR/im); break
            if local_image: st.image(local_image,use_container_width=True)
            else: st.markdown('<div class="product-image">✦</div>',unsafe_allow_html=True)
            st.markdown(f'<div class="product-meta">{html.escape(p.get("category",""))}</div><div class="product-name">{html.escape(p.get("name",""))}</div><div class="price">{money(p.get("price",0))}'+(f'<span class="old-price">{money(p.get("old_price",0))}</span>' if p.get("old_price",0)>p.get("price",0) else '')+'</div>',unsafe_allow_html=True)
            if p.get("sold") or int(p.get("stock",0))<=0:
                st.markdown('<span class="stock sold">SOLD OUT</span>',unsafe_allow_html=True)
                st.button("Unavailable",key=f"unavail_{p['id']}",disabled=True,use_container_width=True)
            else:
                if int(p.get("stock",0))<=3:
                    st.markdown('<span class="stock">LIMITED STOCK</span>',unsafe_allow_html=True)
                else:
                    st.markdown('<span class="stock">AVAILABLE</span>',unsafe_allow_html=True)
                with st.expander("View details"):
                    st.write(p.get("description",""))
                    for im in images:
                        if img_src(im): st.image(im,use_container_width=True)
                    qty=st.number_input("Quantity",min_value=1,max_value=int(p["stock"]),value=1,key=f"addqty_{p['id']}")
                    if st.button("Add to bag",key=f"add_{p['id']}",use_container_width=True):
                        current=int(st.session_state.cart.get(str(p["id"]),0))
                        if current+int(qty)>int(p["stock"]): st.error("That quantity is not currently available.")
                        else:
                            st.session_state.cart[str(p["id"])]=current+int(qty)
                            st.success("Added to your bag.")
            st.markdown("<hr>",unsafe_allow_html=True)

st.markdown(f'<div class="footer">© {html.escape(BRAND)} · Thoughtfully dressed, beautifully you.<br><br>For product enquiries, use the WhatsApp contact configured by the store.</div>',unsafe_allow_html=True)
