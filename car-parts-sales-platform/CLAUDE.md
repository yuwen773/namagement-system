# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Car Parts Sales & Recommendation Platform** - A Django + Vue.js e-commerce platform focused on automotive modification parts with personalized recommendation features.

**Status:** Planning/Documentation Phase (No implementation code exists yet)

**Documentation:** See `PRD.md`, `pre-prd.md`, and `tech-stack.md` for detailed requirements.

## IMPORTANT: 
### Always read memory-bank/@architecture.md before writing any code. Include entire database schema.
### Always read memory-bank/@PRD.md before writing any code.
### After adding a major feature or completing a milestone, update memory-bank/@architecture.md.

## Planned Technology Stack

### Backend
- **Django 5.2+** - Core web framework with ORM and admin panel
- **Django REST Framework** - RESTful API layer for frontend-backend separation
- **MySQL 8.0+** - Relational database

### Frontend
- **Vue.js 3.x** - Progressive JavaScript framework (Composition API)
- **Element Plus** - Vue 3 desktop UI component library
- **ECharts** - Data visualization for marketing/analytics
- **Tailwind CSS** - Utility-first CSS framework

### Development Requirements
- Python 3.10+
- Node.js LTS (18+/20+)

## Planned Django Apps Architecture

The system is organized into two main user interfaces with specific module ordering requirements:

### Platform Admin Modules (Order Must Be Preserved)

1. **商品管理模块** (Product Management)
   - Product CRUD with images, attributes, inventory
   - Multi-level category management
   - Product attribute management (vehicle compatibility, material, color)
   - Product review/publishing workflow

2. **用户与权限管理模块** (User & Permission Management)
   - User list with registration info (nickname, phone, registration date)
   - User details: address book, points status
   - Account status control (ban/unban)

3. **订单与交易管理模块** (Order & Transaction Management)
   - Order management with status filtering (pending payment, pending shipment, shipped, completed, cancelled)
   - Shipping processing (logistics company, tracking number)
   - Return/refund request processing
   - Transaction record queries

4. **营销活动管理模块** (Marketing Activity Management)
   - Coupon management (threshold discount, percentage discount)
   - Coupon settings: validity period, total quantity, per-user limit
   - Promotion activity configuration
   - Marketing material management (banners, posters)
   - Marketing statistics (coupon redemption rate, sales analysis)

5. **推荐管理模块** (Recommendation Management)
   - Recommendation rules configuration (hot items, new arrivals, collaborative filtering)
   - Manual recommendation content management
   - Recommendation monitoring and analytics

6. **系统管理模块** (System Management)
   - Modification case management (articles/images for community building)
   - Knowledge base management (FAQ)
   - System parameter configuration (site name, SEO)
   - Message notification publishing
   - Operation logging for audit trails

### Regular User Modules

1. User registration & login
2. Profile & security management (nickname, avatar, password)
3. Address management (CRUD, default address)
4. Product browsing & reviews (filtering, sorting, 1-5 star ratings with images)
5. Order management (cart → checkout → shipping → tracking)
6. Return/refund applications (reason, evidence upload, progress tracking)
7. Coupon usage (coupon center, application at checkout)

## Data Scale Requirements

### Product Data
- **Minimum 1,000 car modification parts**
- Each product requires: complete attributes, at least 1 clear image

### User Simulation Data
- **~20 active user accounts**
- Each user needs: multiple browsing records, shopping cart entries, order records, reviews

## Core Business Workflows

1. **Product Listing:** Admin publishes parts (images + attributes) → Review → Publish
2. **Browsing & Recommendation:** User browses → System recommends related products
3. **Transaction:** Order → Payment (simulated) → Admin ships → User receives → Review
4. **After-sales:** Return/refund request → Admin review → Process

## Security Requirements

- Password encryption (PBKDF2 or Argon2)
- Protection against: CSRF, XSS, SQL injection
- Response time: < 2 seconds for page loads

## Implementation Priorities

When implementing this project:

1. **Preserve module order** - Admin modules must follow the numbered sequence above
2. **Seed realistic data** - 1,000+ products with images, 20+ users with interaction history
3. **Implement recommendation logic** - Hot items, new arrivals, collaborative filtering parameters
4. **Complete transaction loop** - Full order lifecycle from cart to delivery confirmation
