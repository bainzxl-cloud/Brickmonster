// Simple Stripe Checkout for BrickMonster
// This is a demo showing how to integrate Stripe

// FOR A STATIC SITE, YOU HAVE 2 OPTIONS:

// OPTION 1: Stripe Payment Links (EASIEST - NO CODE)
// ================================================
// 1. Go to Stripe Dashboard → Products
// 2. Create products for your LEGO sets
// 3. For each product, click "Create Payment Link"
// 4. Copy the link and add to your site like: <a href="PAYMENT_LINK">Buy Now</a>

// OPTION 2: Stripe Checkout with Serverless (RECOMMENDED)
// ======================================================
// This file shows how to integrate with Stripe Checkout
// You'll need a simple backend (Cloudflare Workers, Vercel, Netlify, etc.)

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async (event) => {
  const { productId, price } = JSON.parse(event.body);
  
  // Create checkout session
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{
      price_data: {
        currency: 'cad',
        product_data: {
          name: 'LEGO Set',
          description: `Product ID: ${productId}`,
        },
        unit_amount: price * 100, // Stripe uses cents
      },
      quantity: 1,
    }],
    mode: 'payment',
    success_url: 'https://brickmonster.store/success.html',
    cancel_url: 'https://brickmonster.store/cancel.html',
  });

  return {
    statusCode: 200,
    body: JSON.stringify({ url: session.url }),
  };
};
