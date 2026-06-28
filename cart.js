/* =========================================================
   SPLAT — Shared Cart System (localStorage based)
   Include this file on every page via:
   <script src="cart.js"></script>
   ========================================================= */

(function () {
  const CART_KEY = 'splat_cart_v1';

  /* ---------- Storage helpers ---------- */
  function getCart() {
    try {
      const raw = localStorage.getItem(CART_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }

  function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateCartUI();
  }

  function addToCart(item) {
    // item: { id, name, price, img }
    const cart = getCart();
    if (cart.some(v => v.id === item.id)) {
      // already in cart — do nothing (or could show a toast)
      openCartPopup();
      updateCartUI();
      return;
    }
    cart.push(item);
    saveCart(cart);
    openCartPopup();
  }

  function removeFromCart(id) {
    const cart = getCart().filter(v => v.id !== id);
    saveCart(cart);
  }

  function clearCart() {
    saveCart([]);
  }

  function cartTotal() {
    return getCart().reduce((sum, v) => sum + (parseFloat(v.price) || 0), 0);
  }

  /* ---------- UI injection ---------- */
  function injectCartUI() {
    if (document.getElementById('cart-wrap')) return; // already injected

    const headerLeft = document.querySelector('.header-left');
    if (!headerLeft) return;

    const style = document.createElement('style');
    style.textContent = `
      header { justify-content: space-between !important; }
      .cart-wrap { position: relative; }
      .cart-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        background: none;
        border: none;
        cursor: pointer;
        border-radius: 4px;
        position: relative;
        transition: background 0.15s;
      }
      .cart-btn:hover { background: var(--gray); }
      .cart-btn svg { width: 22px; height: 22px; stroke: var(--black); fill: none; stroke-width: 1.8; }
      .cart-badge {
        position: absolute;
        top: 2px;
        right: 2px;
        background: var(--green, #32CD32);
        color: #fff;
        font-size: 10px;
        font-weight: 700;
        min-width: 16px;
        height: 16px;
        padding: 0 4px;
        border-radius: 8px;
        display: none;
        align-items: center;
        justify-content: center;
        line-height: 1;
        font-family: Arial, sans-serif;
      }
      .cart-badge.show { display: flex; }

      /* Cart sidebar overlay */
      .cart-overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        right: 260px;
        bottom: 0;
        background: rgba(0,0,0,0.35);
        z-index: 290;
      }
      .cart-overlay.open { display: block; }

      .cart-popover {
        display: none;
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        width: 260px;
        max-height: none;
        overflow-y: auto;
        background: var(--white, #fff);
        border-left: 1px solid var(--gray-mid, #e0e0e0);
        border-radius: 0;
        box-shadow: -4px 0 20px rgba(0,0,0,0.15);
        z-index: 300;
        padding: 0;
        flex-direction: column;
      }
      .cart-popover.open { display: flex; }
      .cart-popover-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 20px 16px;
        border-bottom: 1px solid var(--gray-mid, #e0e0e0);
      }
      .cart-popover-close {
        background: none;
        border: none;
        font-size: 20px;
        cursor: pointer;
        color: var(--black, #111);
        line-height: 1;
        padding: 4px;
        transition: color 0.15s;
      }
      .cart-popover-close:hover { color: var(--green, #32CD32); }
      .cart-popover-body {
        flex: 1;
        overflow-y: auto;
        padding: 16px 20px;
      }
      .cart-popover-title {
        font-size: 14px;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: var(--black, #111);
        font-weight: 700;
        margin: 0;
      }
      .cart-empty {
        font-size: 13px;
        color: var(--gray-text, #888);
        text-align: center;
        padding: 20px 0;
      }
      .cart-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 0;
        border-bottom: 1px solid var(--gray-mid, #e0e0e0);
      }
      .cart-item:last-of-type { border-bottom: none; }
      .cart-item img {
        width: 48px;
        height: 32px;
        object-fit: cover;
        border-radius: 4px;
        flex-shrink: 0;
        background: var(--gray, #f5f5f5);
      }
      .cart-item-info { flex: 1; min-width: 0; }
      .cart-item-name {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--black, #111);
        line-height: 1.3;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
      }
      .cart-item-price {
        font-size: 11px;
        font-weight: 700;
        color: var(--green-dark, #1db029);
        margin-top: 2px;
      }
      .cart-item-remove {
        background: none;
        border: none;
        cursor: pointer;
        color: var(--gray-text, #888);
        font-size: 16px;
        padding: 4px;
        line-height: 1;
        flex-shrink: 0;
      }
      .cart-item-remove:hover { color: #c00; }
      .cart-footer {
        margin-top: 0;
        padding: 16px 20px 20px;
        border-top: 1px solid var(--gray-mid, #e0e0e0);
      }
      .cart-total-row {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        font-weight: 700;
        color: var(--black, #111);
        margin-bottom: 10px;
      }
      .cart-clear-btn {
        width: 100%;
        background: none;
        border: 1px solid var(--gray-mid, #e0e0e0);
        border-radius: 6px;
        padding: 8px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: var(--gray-text, #888);
        cursor: pointer;
        transition: border-color 0.15s, color 0.15s;
      }
      .cart-clear-btn:hover { border-color: #c00; color: #c00; }
      .cart-pay-btn {
        display: block;
        width: 100%;
        background: var(--black, #111);
        color: var(--white, #fff);
        border: none;
        border-radius: 6px;
        padding: 10px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        text-align: center;
        text-decoration: none;
        cursor: pointer;
        margin-bottom: 8px;
        transition: background 0.18s;
      }
      .cart-pay-btn:hover { background: #333; }
      @media (prefers-color-scheme: dark) {
        .cart-btn svg { stroke: #f0f0f0; }
        .cart-popover { background: #0d0d0d; border-left-color: #333; }
        .cart-popover-header { border-bottom-color: #333; }
        .cart-popover-title { color: #f0f0f0; }
        .cart-popover-close { color: #f0f0f0; }
        .cart-item { border-bottom-color: #333; }
        .cart-footer { border-top-color: #333; }
        .cart-clear-btn { border-color: #444; color: #999; }
        .cart-pay-btn { background: #f0f0f0; color: #111; }
        .cart-pay-btn:hover { background: #ddd; }
        .cart-overlay { background: rgba(0,0,0,0.55); }
      }
      @media (max-width: 600px) {
        .cart-popover { width: 260px; }
        .cart-overlay { right: 260px; }
      }
    `;
    document.head.appendChild(style);

    const cartOverlay = document.createElement('div');
    cartOverlay.className = 'cart-overlay';
    cartOverlay.id = 'cart-overlay';
    document.body.appendChild(cartOverlay);

    const cartWrap = document.createElement('div');
    cartWrap.className = 'cart-wrap';
    cartWrap.id = 'cart-wrap';
    cartWrap.innerHTML = `
      <button class="cart-btn" id="cart-btn" aria-label="Cart">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
        <span class="cart-badge" id="cart-badge"></span>
      </button>
      <div class="cart-popover" id="cart-popover">
        <div class="cart-popover-header">
          <div class="cart-popover-title">Your Cart</div>
          <button class="cart-popover-close" onclick="window.SplatCart.closePopup()" aria-label="Close">✕</button>
        </div>
        <div class="cart-popover-body">
          <div id="cart-items"></div>
        </div>
        <div class="cart-footer" id="cart-footer" style="display:none;">
          <div class="cart-total-row">
            <span>Total</span>
            <span id="cart-total-value">$0 USD</span>
          </div>
          <a class="cart-pay-btn" id="cart-pay-btn" href="https://www.paypal.com/paypalme/splatmessydares" target="_blank" rel="noopener noreferrer">Pay Now</a>
          <button class="cart-clear-btn" id="cart-clear-btn">Clear All</button>
        </div>
      </div>
    `;
    headerLeft.parentElement.appendChild(cartWrap);

    document.getElementById('cart-btn').addEventListener('click', function (e) {
      e.stopPropagation();
      toggleCartPopup();
    });
    document.getElementById('cart-clear-btn').addEventListener('click', function (e) {
      e.stopPropagation();
      clearCart();
    });
    cartOverlay.addEventListener('click', function () {
      closeCartPopup();
    });
  }

  function toggleCartPopup() {
    document.getElementById('cart-popover').classList.toggle('open');
    document.getElementById('cart-overlay').classList.toggle('open');
  }
  function openCartPopup() {
    document.getElementById('cart-popover').classList.add('open');
    document.getElementById('cart-overlay').classList.add('open');
  }
  function closeCartPopup() {
    const pop = document.getElementById('cart-popover');
    const overlay = document.getElementById('cart-overlay');
    if (pop) pop.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
  }

  function updateCartUI() {
    const cart = getCart();
    const badge = document.getElementById('cart-badge');
    const itemsWrap = document.getElementById('cart-items');
    const footer = document.getElementById('cart-footer');
    const totalValue = document.getElementById('cart-total-value');
    if (!badge || !itemsWrap) return;

    if (cart.length > 0) {
      badge.textContent = cart.length;
      badge.classList.add('show');
    } else {
      badge.classList.remove('show');
    }

    if (cart.length === 0) {
      itemsWrap.innerHTML = '<div class="cart-empty">Your cart is empty</div>';
      footer.style.display = 'none';
      return;
    }

    itemsWrap.innerHTML = cart.map(v => `
      <div class="cart-item">
        <img src="${v.img}" alt="${v.name}" />
        <div class="cart-item-info">
          <div class="cart-item-name">${v.name}</div>
          <div class="cart-item-price">$${v.price} USD</div>
        </div>
        <button class="cart-item-remove" data-id="${v.id}" aria-label="Remove">✕</button>
      </div>
    `).join('');

    itemsWrap.querySelectorAll('.cart-item-remove').forEach(btn => {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        removeFromCart(this.dataset.id);
      });
    });

    footer.style.display = 'block';
    totalValue.textContent = `$${cartTotal()} USD`;
  }

  /* ---------- Public API ---------- */
  window.SplatCart = {
    add: addToCart,
    remove: removeFromCart,
    clear: clearCart,
    getAll: getCart,
    total: cartTotal,
    closePopup: closeCartPopup
  };

  /* ---------- Init on DOM ready ---------- */
  function init() {
    injectCartUI();
    updateCartUI();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();