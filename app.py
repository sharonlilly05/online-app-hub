from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

# Models
class ExternalShop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    logo_url = db.Column(db.String(200), nullable=False)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ExternalStudy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    logo_url = db.Column(db.String(200))
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ExternalMessaging(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    logo_url = db.Column(db.String(200))
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ExternalMusic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    logo_url = db.Column(db.String(200))
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ExternalFitness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    logo_url = db.Column(db.String(200))
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ExternalSocial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    logo_url = db.Column(db.String(200))
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    user_session = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

@app.route('/')
def home():
    # Return a simple HTML front page (inline) to avoid current template-loader issues
    parts = []
    parts.append('<div class="hero"><div class="hero-inner"><h2>Online App Hub</h2></div></div>')
    parts.append('<div class="card-container">')
    parts.append(f'<a href="{url_for("ecommerce_app")}" class="card"><div class="card-icon">🛒</div><h3>E-Commerce</h3></a>')
    parts.append(f'<a href="{url_for("study_app")}" class="card"><div class="card-icon">📚</div><h3>Study Hub</h3></a>')
    parts.append(f'<a href="{url_for("messaging_app")}" class="card"><div class="card-icon">💬</div><h3>Messaging</h3></a>')
    parts.append(f'<a href="{url_for("music_app")}" class="card"><div class="card-icon">🎵</div><h3>Music Stream</h3></a>')
    parts.append(f'<a href="{url_for("fitness_app")}" class="card"><div class="card-icon">💪</div><h3>Fitness Pro</h3></a>')
    parts.append(f'<a href="{url_for("social_app")}" class="card"><div class="card-icon">🐦</div><h3>Social Media</h3></a>')
    parts.append('</div>')
    parts.append('<div class="page-links"><a href="/home">Home</a><a href="/about">About</a><a href="/contact">Contact</a></div>')
    parts.append('<footer class="site-footer"><p>© 2026 Online App Hub | Built with Flask</p></footer>')

    body = '\n'.join(parts)
    html = f"<!doctype html><html><head><meta charset=\"utf-8\"><title>Online App Hub</title>\n"
    html += "<link rel=\"stylesheet\" href=\"/static/style.css\">\n</head><body>"
    html += body
    html += "</body></html>"
    return html

@app.route('/home')
def home_page():
    return render_template('home.html', title='Home')

@app.route('/about')
def about_page():
    return render_template('about.html', title='About Us')

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        flash('Thanks for reaching out! We will get back to you soon.')
        return redirect(url_for('contact_page'))
    return render_template('contact.html', title='Contact Us')

# ---------- E-COMMERCE ----------
@app.route('/ecommerce')
def ecommerce_app():
    # Build a simple HTML response directly (bypass Jinja templates) so
    # clicking a shop link goes straight to the external marketplace.
    remove_names = ['Laptop', 'Smartphone', 'Headphones', 'T-Shirt', 'Jeans']
    products = [p for p in Product.query.all() if p.name not in remove_names]
    external_shops = ExternalShop.query.order_by(ExternalShop.clicks.desc()).all()

    # Build HTML inline (workaround for current template/loader issues) but use the
    # same classes as `ecommerce_app.html` so CSS/layout remain identical.
    parts = []
    parts.append('<h2>Our Products</h2>')
    parts.append('<p>Explore our products and popular shopping platforms below.</p>')

    parts.append('<section class="external-shops">')
    parts.append('<h3>Shop on Popular Platforms</h3>')
    parts.append('<div class="shop-links">')
    for shop in external_shops:
        link = url_for('external_shop_redirect', shop_id=shop.id)
        logo = shop.logo_url or ''
        if logo:
            parts.append(
                f'<a href="{link}" target="_blank" rel="noopener noreferrer" class="shop-link">'
                f'<img src="{logo}" alt="{shop.name} logo" class="shop-logo" '
                f'onerror="this.style.display=\'none\';this.parentNode.querySelector(\'.shop-name-fallback\').style.display=\'inline-block\';" '
                f'onload="this.parentNode.querySelector(\'.shop-name-fallback\').style.display=\'none\';">'
                f'<div class="shop-name-fallback" style="display:none">{shop.name}</div>'
                f'<div class="shop-meta"><div class="shop-name">Shop on {shop.name}</div></div>'
                f'</a>'
            )
        else:
            parts.append(
                f'<a href="{link}" target="_blank" rel="noopener noreferrer" class="shop-link">'
                f'<div class="shop-name-fallback">{shop.name}</div>'
                f'<div class="shop-meta"><div class="shop-name">Shop on {shop.name}</div></div>'
                f'</a>'
            )
    parts.append('</div>')
    parts.append('</section>')

    # Products grid (only render if products exist)
    if products:
        parts.append('<hr>')
        parts.append('<section class="product-grid">')
        for p in products:
            parts.append('<div class="product-card">')
            if p.image_url:
                parts.append(f'<img src="{p.image_url}" alt="{p.name}" class="product-image">')
            parts.append(f'<h3>{p.name}</h3>')
            parts.append(f'<p class="price">₹{p.price:.2f}</p>')
            parts.append(f'<p class="description">{(p.description or "")}</p>')
            parts.append('<div class="product-actions">')
            parts.append(f'<a href="{url_for("ecommerce_detail", product_id=p.id)}" class="btn btn-primary">View Details</a>')
            parts.append('</div>')
            parts.append('</div>')
        parts.append('</section>')

    body = '\n'.join(parts)
    html = f"<!doctype html><html><head><meta charset=\"utf-8\"><title>E-Commerce</title>\n"
    html += "<link rel=\"stylesheet\" href=\"/static/style.css\">\n</head><body>"
    html += body
    html += "</body></html>"
    return html

@app.route('/external_shop/<int:shop_id>')
def external_shop_redirect(shop_id):
    shop = ExternalShop.query.get_or_404(shop_id)
    shop.clicks += 1
    db.session.commit()
    return redirect(shop.url)

@app.route('/ecommerce/detail/<int:product_id>')
def ecommerce_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('ecommerce_detail.html', product=product)

@app.route('/cart')
def cart():
    session_id = request.cookies.get('session_id', 'default_session')
    cart_items = CartItem.query.filter_by(user_session=session_id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    session_id = request.cookies.get('session_id', 'default_session')
    quantity = int(request.form.get('quantity', 1))
    
    cart_item = CartItem.query.filter_by(
        product_id=product_id,
        user_session=session_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            product_id=product_id,
            quantity=quantity,
            user_session=session_id
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Item added to cart successfully!')
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart!')
    return redirect(url_for('cart'))

@app.route('/update_cart/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        db.session.commit()
        flash('Cart updated successfully!')
    elif quantity == 0:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart!')
    
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    session_id = request.cookies.get('session_id', 'default_session')
    cart_items = CartItem.query.filter_by(user_session=session_id).all()
    
    if not cart_items:
        flash('Your cart is empty!')
        return redirect(url_for('cart'))
    
    # In a real application, you would:
    # 1. Process payment
    # 2. Create an order in the database
    # 3. Send confirmation email
    # 4. Clear the cart
    
    # For now, we'll just clear the cart
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()
    
    flash('Thank you for your purchase! Your order has been placed.')
    return redirect(url_for('ecommerce_app'))

# ---------- STUDY HUB ----------
@app.route('/study')
def study_app():
    # Build inline HTML for the Study Hub using the same block layout as ecommerce
    external_studies = ExternalStudy.query.order_by(ExternalStudy.clicks.desc()).all()

    parts = []
    parts.append('<h2>Study Apps</h2>')
    parts.append('<p>Boost your learning with these study tools.</p>')
    parts.append('<section class="external-studies">')
    parts.append('<h3>Popular Study Apps</h3>')
    parts.append('<div class="study-links">')
    for s in external_studies:
        link = url_for('external_study_redirect', study_id=s.id)
        logo = s.logo_url or ''
        if logo:
            parts.append(
                f'<a href="{link}" target="_blank" rel="noopener noreferrer" class="shop-link">'
                f'<img src="{logo}" alt="{s.name} logo" class="shop-logo" '
                f'onerror="this.style.display=\'none\';this.parentNode.querySelector(\'.shop-name-fallback\').style.display=\'inline-block\';" '
                f'onload="this.parentNode.querySelector(\'.shop-name-fallback\').style.display=\'none\';">'
                f'<div class="shop-name-fallback" style="display:none">{s.name}</div>'
                f'<div class="shop-meta"><div class="shop-name">Study on {s.name}</div></div>'
                f'</a>'
            )
        else:
            parts.append(
                f'<a href="{link}" target="_blank" rel="noopener noreferrer" class="shop-link">'
                f'<div class="shop-name-fallback">{s.name}</div>'
                f'<div class="shop-meta"><div class="shop-name">Study on {s.name}</div></div>'
                f'</a>'
            )
    parts.append('</div>')
    parts.append('</section>')

    body = '\n'.join(parts)
    html = f"<!doctype html><html><head><meta charset=\"utf-8\"><title>Study Hub</title>\n"
    html += "<link rel=\"stylesheet\" href=\"/static/style.css\">\n</head><body>"
    html += body
    html += "</body></html>"
    return html

@app.route('/study/<app_name>')
def study_detail(app_name):
    details = {
        "notion": "Notion helps organize study notes, projects, and tasks in one place.",
        "coursera": "Coursera offers online courses and certifications from top universities.",
        "duolingo": "Duolingo helps learn new languages with fun, gamified lessons."
    }
    info = details.get(app_name.lower(), "Details not available.")
    return render_template('study_detail.html', app_name=app_name.title(), info=info)


@app.route('/external_study/<int:study_id>')
def external_study_redirect(study_id):
    study = ExternalStudy.query.get_or_404(study_id)
    study.clicks += 1
    db.session.commit()
    return redirect(study.url)

# ---------- MESSAGING ----------
@app.route('/messaging')
def messaging_app():
    # Build inline HTML for messaging using the same block layout as study/ecommerce
    external_messaging = ExternalMessaging.query.order_by(ExternalMessaging.clicks.desc()).all()
    parts = []
    parts.append('<h2>Messaging Apps</h2>')
    parts.append('<p>Popular messaging apps to stay connected with friends, family, and colleagues.</p>')
    parts.append('<section class="external-messaging">')
    parts.append('<h3>Popular Messaging Apps</h3>')
    parts.append('<div class="study-links">')
    for m in external_messaging:
        link = url_for('external_messaging_redirect', messaging_id=m.id)
        logo = m.logo_url or ''
        if logo:
            parts.append(
                f'<a href="{link}" target="_blank" rel="noopener noreferrer" class="shop-link">'
                f'<img src="{logo}" alt="{m.name} logo" class="shop-logo" '
                f'onerror="this.style.display=\'none\';this.parentNode.querySelector(\'.shop-name-fallback\').style.display=\'inline-block\';" '
                f'onload="this.parentNode.querySelector(\'.shop-name-fallback\').style.display=\'none\';">'
                f'<div class="shop-name-fallback" style="display:none">{m.name}</div>'
                f'<div class="shop-meta"><div class="shop-name">{m.name}</div></div>'
                f'</a>'
            )
        else:
            parts.append(
                f'<a href="{link}" target="_blank" rel="noopener noreferrer" class="shop-link">'
                f'<div class="shop-name-fallback">{m.name}</div>'
                f'<div class="shop-meta"><div class="shop-name">{m.name}</div></div>'
                f'</a>'
            )
    parts.append('</div>')
    parts.append('</section>')
    body = '\n'.join(parts)
    html = f"<!doctype html><html><head><meta charset=\"utf-8\"><title>Messaging</title>\n"
    html += "<link rel=\"stylesheet\" href=\"/static/style.css\">\n</head><body>"
    html += body
    html += "</body></html>"
    return html

@app.route('/messaging/<app_name>')
def messaging_detail(app_name):
    details = {
        "whatsapp": "WhatsApp enables free messaging, calling, and file sharing globally.",
        "telegram": "Telegram offers cloud-based messaging with privacy-focused features.",
        "signal": "Signal provides secure encrypted messaging and calls."
    }
    info = details.get(app_name.lower(), "Details not available.")
    return render_template('messaging_detail.html', app_name=app_name.title(), info=info)

@app.route('/external_messaging/<int:messaging_id>')
def external_messaging_redirect(messaging_id):
    messaging = ExternalMessaging.query.get_or_404(messaging_id)
    messaging.clicks += 1
    db.session.commit()
    return redirect(messaging.url)

# ---------- MUSIC STREAM ----------
@app.route('/music')
def music_app():
    # Build inline HTML for music using the same block layout
    external_music = ExternalMusic.query.order_by(ExternalMusic.clicks.desc()).all()
    parts = []
    parts.append('<h2>Music Apps</h2>')
    parts.append('<p>Stream your favorite music and podcasts anytime.</p>')
    parts.append('<section class="external-music">')
    parts.append('<h3>Popular Music Apps</h3>')
    parts.append('<div class="study-links">')
    for m in external_music:
        link = url_for('external_music_redirect', music_id=m.id)
        logo = m.logo_url or ''
        if logo:
            parts.append(
                f'<a href="{link}" target="_blank" rel="noopener noreferrer" class="shop-link">'
                f'<img src="{logo}" alt="{m.name} logo" class="shop-logo" '
                f'onerror="this.style.display=\'none\';this.parentNode.querySelector(\'.shop-name-fallback\').style.display=\'inline-block\';" '
                f'onload="this.parentNode.querySelector(\'.shop-name-fallback\').style.display=\'none\';">'
                f'<div class="shop-name-fallback" style="display:none">{m.name}</div>'
                f'<div class="shop-meta"><div class="shop-name">{m.name}</div></div>'
                f'</a>'
            )
        else:
            parts.append(
                f'<a href="{link}" target="_blank" rel="noopener noreferrer" class="shop-link">'
                f'<div class="shop-name-fallback">{m.name}</div>'
                f'<div class="shop-meta"><div class="shop-name">{m.name}</div></div>'
                f'</a>'
            )
    parts.append('</div>')
    parts.append('</section>')
    body = '\n'.join(parts)
    html = f"<!doctype html><html><head><meta charset=\"utf-8\"><title>Music Stream</title>\n"
    html += "<link rel=\"stylesheet\" href=\"/static/style.css\">\n</head><body>"
    html += body
    html += "</body></html>"
    return html

@app.route('/music/<app_name>')
def music_detail(app_name):
    details = {
        "spotify": "Spotify streams millions of songs and podcasts globally.",
        "gaana": "Gaana offers Indian and international music streaming with playlists.",
        "youtube music": "YouTube Music provides video and audio-based music access."
    }
    info = details.get(app_name.lower(), "Details not available.")
    return render_template('music_detail.html', app_name=app_name.title(), info=info)

@app.route('/external_music/<int:music_id>')
def external_music_redirect(music_id):
    music = ExternalMusic.query.get_or_404(music_id)
    music.clicks += 1
    db.session.commit()
    return redirect(music.url)

# ---------- FITNESS PRO ----------
@app.route('/fitness')
def fitness_app():
    # Build inline HTML for fitness using the same block layout
    external_fitness = ExternalFitness.query.order_by(ExternalFitness.clicks.desc()).all()
    parts = []
    parts.append('<h2>Fitness Apps</h2>')
    parts.append('<p>Track workouts and stay fit with these amazing apps.</p>')
    parts.append('<section class="external-fitness">')
    parts.append('<h3>Popular Fitness Apps</h3>')
    parts.append('<div class="study-links">')
    for f in external_fitness:
        link = url_for('external_fitness_redirect', fitness_id=f.id)
        logo = f.logo_url or ''
        if logo:
            parts.append(
                f'<a href="{link}" target="_blank" rel="noopener noreferrer" class="shop-link">'
                f'<img src="{logo}" alt="{f.name} logo" class="shop-logo" '
                f'onerror="this.style.display=\'none\';this.parentNode.querySelector(\'.shop-name-fallback\').style.display=\'inline-block\';" '
                f'onload="this.parentNode.querySelector(\'.shop-name-fallback\').style.display=\'none\';">'
                f'<div class="shop-name-fallback" style="display:none">{f.name}</div>'
                f'<div class="shop-meta"><div class="shop-name">{f.name}</div></div>'
                f'</a>'
            )
        else:
            parts.append(
                f'<a href="{link}" target="_blank" rel="noopener noreferrer" class="shop-link">'
                f'<div class="shop-name-fallback">{f.name}</div>'
                f'<div class="shop-meta"><div class="shop-name">{f.name}</div></div>'
                f'</a>'
            )
    parts.append('</div>')
    parts.append('</section>')
    body = '\n'.join(parts)
    html = f"<!doctype html><html><head><meta charset=\"utf-8\"><title>Fitness Pro</title>\n"
    html += "<link rel=\"stylesheet\" href=\"/static/style.css\">\n</head><body>"
    html += body
    html += "</body></html>"
    return html

@app.route('/fitness/<app_name>')
def fitness_detail(app_name):
    details = {
        "fittr": "Fittr offers personalized fitness and nutrition coaching.",
        "cultfit": "Cult Fit provides fitness classes, yoga, and mental wellness sessions.",
        "healthifyme": "HealthifyMe tracks calories and provides AI fitness guidance."
    }
    info = details.get(app_name.lower(), "Details not available.")
    return render_template('fitness_detail.html', app_name=app_name.title(), info=info)

@app.route('/external_fitness/<int:fitness_id>')
def external_fitness_redirect(fitness_id):
    fitness = ExternalFitness.query.get_or_404(fitness_id)
    fitness.clicks += 1
    db.session.commit()
    return redirect(fitness.url)

# ---------- SOCIAL MEDIA ----------
@app.route('/social')
def social_app():
    # Inline HTML for social hub
    external_social = ExternalSocial.query.order_by(ExternalSocial.clicks.desc()).all()
    parts = []
    parts.append('<h2>Social Media</h2>')
    parts.append('<p>Popular social networks.</p>')
    parts.append('<section class="social-list"><div class="social-links">')
    for s in external_social:
        link = url_for('external_social_redirect', social_id=s.id)
        logo = s.logo_url or ''
        if logo:
            parts.append(f"<a href=\"{link}\" target=\"_blank\" rel=\"noopener noreferrer\">"
                         f"<img src=\"{logo}\" alt=\"{s.name} logo\" style=\"height:36px;vertical-align:middle;margin-right:8px\"/>"
                         f"{s.name}</a>")
        else:
            parts.append(f"<a href=\"{link}\" target=\"_blank\">{s.name}</a>")
    parts.append('</div></section>')
    body = '\n'.join(parts)
    html = f"<!doctype html><html><head><meta charset=\"utf-8\"><title>Social Media</title>\n"
    html += "<link rel=\"stylesheet\" href=\"/static/style.css\">\n</head><body>"
    html += body
    html += "</body></html>"
    return html

@app.route('/social/<app_name>')
def social_detail(app_name):
    details = {
        "instagram": "Instagram is a photo and video sharing platform.",
        "twitter": "Twitter (X) is used for short messages, updates, and trends.",
        "facebook": "Facebook connects people, communities, and businesses online."
    }
    info = details.get(app_name.lower(), "Details not available.")
    return render_template('social_detail.html', app_name=app_name.title(), info=info)

@app.route('/external_social/<int:social_id>')
def external_social_redirect(social_id):
    social = ExternalSocial.query.get_or_404(social_id)
    social.clicks += 1
    db.session.commit()
    return redirect(social.url)


def init_external_shops():
    # First, delete all existing shops
    ExternalShop.query.delete()
    db.session.commit()
    
    # Add shops fresh
    shops = [
        {
            'name': 'Amazon',
            'url': 'https://www.amazon.in',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/1200px-Amazon_logo.svg.png'
        },
        {
            'name': 'Flipkart',
            'url': 'https://www.flipkart.com',
            'logo_url': 'https://logos-world.net/wp-content/uploads/2020/11/Flipkart-Logo.png'
        },
        {
            'name': 'Meesho',
            'url': 'https://www.meesho.com',
            'logo_url': 'https://play-lh.googleusercontent.com/3yi7Fo-OtJUZ7nAlB8WB0v1WTOdz76Z1kqvuuubhNlHzU9jhP97TnI-6eVThWZMV31A'
        },
        {
            'name': 'Myntra',
            'url': 'https://www.myntra.com',
            'logo_url': '/static/images/myntra.jpg'
        },
        {
            'name': 'Ajio',
            'url': 'https://www.ajio.com',
            'logo_url': 'https://assets.ajio.com/static/img/Ajio-Logo.svg'
        },
        {
            'name': 'BigBasket',
            'url': 'https://www.bigbasket.com',
            'logo_url': '/static/images/bigbasket.jpg'
        }
    ]

    # Add each shop
    for shop_data in shops:
        shop = ExternalShop(**shop_data)
        db.session.add(shop)

    db.session.commit()


def init_external_studies():
    # First, delete all existing studies to prevent duplicates
    ExternalStudy.query.delete()
    db.session.commit()
    
    # Add fresh study apps with logos from static/images/
    studies = [
        {
            'name': "Byju's",
            'url': 'https://byjus.com',
            'logo_url': '/static/images/byjus.jpg'
        },
        {
            'name': 'Khan Academy',
            'url': 'https://www.khanacademy.org',
            'logo_url': '/static/images/khan-academy.jpg'
        },
        {
            'name': 'Coursera',
            'url': 'https://www.coursera.org',
            'logo_url': '/static/images/coursera.jpg'
        },
        {
            'name': 'Unacademy',
            'url': 'https://unacademy.com',
            'logo_url': '/static/images/unacademy.jpg'
        }
    ]

    for s in studies:
        existing = ExternalStudy.query.filter_by(name=s['name']).first()
        if existing:
            existing.url = s['url']
            existing.logo_url = s.get('logo_url')
        else:
            study = ExternalStudy(**s)
            db.session.add(study)

    db.session.commit()


def init_external_messaging():
    # First, delete all existing messaging apps to prevent duplicates
    ExternalMessaging.query.delete()
    db.session.commit()
    
    # Add fresh messaging apps
    messaging_apps = [
        {
            'name': 'WhatsApp',
            'url': 'https://www.whatsapp.com',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg'
        },
        {
            'name': 'Telegram',
            'url': 'https://telegram.org',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg'
        },
        {
            'name': 'Signal',
            'url': 'https://signal.org',
            'logo_url': '/static/images/messaging/signal.jpg'
        },
        {
            'name': 'Viber',
            'url': 'https://www.viber.com',
            'logo_url': '/static/images/messaging/viber.jpg'
        }
    ]

    # Add each messaging app
    for app_data in messaging_apps:
        app = ExternalMessaging(**app_data)
        db.session.add(app)

    db.session.commit()


def init_external_music():
    # Delete all existing music apps to prevent duplicates
    ExternalMusic.query.delete()
    db.session.commit()
    
    # Add fresh music apps
    music_apps = [
        {
            'name': 'Spotify',
            'url': 'https://www.spotify.com',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/7/74/Spotify_App_Logo.svg'
        },
        {
            'name': 'Gaana',
            'url': 'https://www.gaana.com',
            'logo_url': '/static/images/music/gaana.jpg'
        },
        {
            'name': 'YouTube Music',
            'url': 'https://music.youtube.com',
            # file in static/images/music is named 'youtube.jpg'
            'logo_url': '/static/images/music/youtube.jpg'
        }
    ]

    for app_data in music_apps:
        app = ExternalMusic(**app_data)
        db.session.add(app)

    db.session.commit()


def init_external_fitness():
    # Delete all existing fitness apps to prevent duplicates
    ExternalFitness.query.delete()
    db.session.commit()
    
    # Add fresh fitness apps
    fitness_apps = [
        {
            'name': 'Fittr',
            'url': 'https://www.fittr.com',
            'logo_url': '/static/images/fitness/fittr.jpg'
        },
        {
            'name': 'Cult Fit',
            'url': 'https://www.cult.fit',
            # actual filename copied into static/images/fitness is 'culfit.jpg'
            'logo_url': '/static/images/fitness/culfit.jpg'
        },
        {
            'name': 'HealthifyMe',
            'url': 'https://www.healthifyme.com',
            # actual filename copied into static/images/fitness is 'healthify.jpg'
            'logo_url': '/static/images/fitness/healthify.jpg'
        }
    ]

    for app_data in fitness_apps:
        app = ExternalFitness(**app_data)
        db.session.add(app)

    db.session.commit()


def init_external_social():
    # Delete all existing social apps to prevent duplicates
    ExternalSocial.query.delete()
    db.session.commit()
    
    # Add fresh social media apps
    social_apps = [
        {
            'name': 'Instagram',
            'url': 'https://www.instagram.com',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png'
        },
        {
            'name': 'Twitter',
            'url': 'https://www.twitter.com',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/c/ce/X_logo_2023.svg'
        },
        {
            'name': 'Facebook',
            'url': 'https://www.facebook.com',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/0/05/Facebook_Logo_%282019%29.png'
        }
    ]

    for app_data in social_apps:
        app = ExternalSocial(**app_data)
        db.session.add(app)

    db.session.commit()


# ---------- ADMIN: External Shops & Studies ----------
@app.route('/admin/shops')
def admin_shops():
    shops = ExternalShop.query.order_by(ExternalShop.clicks.desc()).all()
    return render_template('admin_shops.html', shops=shops)


@app.route('/admin/shops/create', methods=['GET', 'POST'])
def admin_create_shop():
    if request.method == 'POST':
        name = request.form.get('name')
        url_ = request.form.get('url')
        logo = request.form.get('logo_url')
        shop = ExternalShop(name=name, url=url_, logo_url=logo)
        db.session.add(shop)
        db.session.commit()
        flash('Shop created successfully!')
        return redirect(url_for('admin_shops'))
    return render_template('admin_shop_form.html', action='Create', shop=None)


@app.route('/admin/shops/edit/<int:shop_id>', methods=['GET', 'POST'])
def admin_edit_shop(shop_id):
    shop = ExternalShop.query.get_or_404(shop_id)
    if request.method == 'POST':
        shop.name = request.form.get('name')
        shop.url = request.form.get('url')
        shop.logo_url = request.form.get('logo_url')
        db.session.commit()
        flash('Shop updated successfully!')
        return redirect(url_for('admin_shops'))
    return render_template('admin_shop_form.html', action='Edit', shop=shop)


@app.route('/admin/shops/delete/<int:shop_id>', methods=['POST'])
def admin_delete_shop(shop_id):
    shop = ExternalShop.query.get_or_404(shop_id)
    db.session.delete(shop)
    db.session.commit()
    flash('Shop deleted.')
    return redirect(url_for('admin_shops'))


@app.route('/admin/studies')
def admin_studies():
    studies = ExternalStudy.query.order_by(ExternalStudy.clicks.desc()).all()
    return render_template('admin_studies.html', studies=studies)


@app.route('/admin/studies/create', methods=['GET', 'POST'])
def admin_create_study():
    if request.method == 'POST':
        name = request.form.get('name')
        url_ = request.form.get('url')
        logo = request.form.get('logo_url')
        study = ExternalStudy(name=name, url=url_, logo_url=logo)
        db.session.add(study)
        db.session.commit()
        flash('Study app created successfully!')
        return redirect(url_for('admin_studies'))
    return render_template('admin_study_form.html', action='Create', study=None)


@app.route('/admin/studies/edit/<int:study_id>', methods=['GET', 'POST'])
def admin_edit_study(study_id):
    study = ExternalStudy.query.get_or_404(study_id)
    if request.method == 'POST':
        study.name = request.form.get('name')
        study.url = request.form.get('url')
        study.logo_url = request.form.get('logo_url')
        db.session.commit()
        flash('Study app updated successfully!')
        return redirect(url_for('admin_studies'))
    return render_template('admin_study_form.html', action='Edit', study=study)


@app.route('/admin/studies/delete/<int:study_id>', methods=['POST'])
def admin_delete_study(study_id):
    study = ExternalStudy.query.get_or_404(study_id)
    db.session.delete(study)
    db.session.commit()
    flash('Study app deleted.')
    return redirect(url_for('admin_studies'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_external_shops()
        init_external_studies()
        init_external_messaging()
        init_external_music()
        init_external_fitness()
        init_external_social()
    app.run(debug=True)