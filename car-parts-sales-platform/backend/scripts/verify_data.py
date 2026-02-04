# -*- coding: utf-8 -*-
"""
Data Verification Script - Phase 4 Step 2

Verify data integrity and quality in the database

Verification items:
1. User count >= 20
2. Product count >= 1000
3. Each product has at least one image
4. Order status distribution is reasonable
5. Foreign key constraints are valid

Usage:
    cd backend
    python scripts/verify_data.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.db.models import Count, Q, Avg, Sum

from apps.users.models import User, UserAddress
from apps.products.models import Category, Product, ProductImage, ProductAttribute, Review
from apps.orders.models import Order, OrderItem, Cart, CartItem
from apps.marketing.models import Coupon, UserCoupon
from apps.recommendations.models import RecommendationRule, RecommendedProduct
from apps.content.models import ModificationCase, FAQ
from apps.system.models import SystemConfig, Message, OperationLog


# ==================== Color Output ====================

class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def print_success(msg):
    """Print success message"""
    print(f"{Colors.GREEN}[OK] {msg}{Colors.RESET}")


def print_error(msg):
    """Print error message"""
    print(f"{Colors.RED}[FAIL] {msg}{Colors.RESET}")


def print_warning(msg):
    """Print warning message"""
    print(f"{Colors.YELLOW}[WARN] {msg}{Colors.RESET}")


def print_info(msg):
    """Print info message"""
    print(f"{Colors.BLUE}[INFO] {msg}{Colors.RESET}")


def print_header(msg):
    """Print header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


# ==================== Verification Functions ====================

class DataValidator:
    """Data validator"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.results = []

    def verify_user_count(self):
        """Verify user count"""
        print_info("Verifying user count...")

        # Verify admin users
        admin_count = User.objects.filter(is_staff=True, is_superuser=True).count()
        if admin_count >= 5:
            print_success(f"Admin users: {admin_count} (>=5)")
            self.passed += 1
        else:
            print_error(f"Admin users: {admin_count} (need >=5)")
            self.failed += 1

        # Verify regular users
        regular_count = User.objects.filter(is_staff=False).count()
        if regular_count >= 20:
            print_success(f"Regular users: {regular_count} (>=20)")
            self.passed += 1
        else:
            print_error(f"Regular users: {regular_count} (need >=20)")
            self.failed += 1

        # Verify user status
        active_users = User.objects.filter(status='active').count()
        print_info(f"Active users: {active_users}")

        return admin_count >= 5 and regular_count >= 20

    def verify_user_addresses(self):
        """Verify user addresses"""
        print_info("Verifying user addresses...")

        # Check if each user has at least one address
        users_without_address = User.objects.filter(
            is_staff=False
        ).annotate(
            addr_count=Count('addresses')
        ).filter(addr_count=0).count()

        if users_without_address == 0:
            print_success("All users have addresses")
            self.passed += 1
            return True
        else:
            print_warning(f"{users_without_address} users have no address")
            self.warnings += 1
            return True

    def verify_categories(self):
        """Verify product categories"""
        print_info("Verifying product categories...")

        total_categories = Category.objects.count()
        if total_categories >= 50:
            print_success(f"Product categories: {total_categories} (>=50)")
            self.passed += 1
            return True
        else:
            print_error(f"Product categories: {total_categories} (need >=50)")
            self.failed += 1
            return False

    def verify_products(self):
        """Verify product data"""
        print_info("Verifying product data...")

        # Verify product count
        product_count = Product.objects.count()
        if product_count >= 1000:
            print_success(f"Product count: {product_count} (>=1000)")
            self.passed += 1
        else:
            print_error(f"Product count: {product_count} (need >=1000)")
            self.failed += 1

        # Verify product status distribution
        status_dist = Product.objects.values('status').annotate(count=Count('id'))
        for item in status_dist:
            status_name = item['status']
            count = item['count']
            print_info(f"  - {status_name}: {count}")

        # Verify price range
        price_stats = Product.objects.aggregate(
            avg_price=Avg('price')
        )
        avg_price = price_stats['avg_price']
        print_info(f"Average price: CNY {avg_price:.2f}" if avg_price else "Average price: N/A")

        return product_count >= 1000

    def verify_product_images(self):
        """Verify product images"""
        print_info("Verifying product images...")

        # Check if each product has at least one image
        products_without_images = Product.objects.filter(
            images__isnull=True
        ).count()

        if products_without_images == 0:
            print_success("All products have images")
            self.passed += 1
        else:
            print_error(f"{products_without_images} products have no images")
            self.failed += 1

        # Count images
        image_count = ProductImage.objects.count()
        print_info(f"Total product images: {image_count}")

        # Average images per product
        avg_images = image_count / Product.objects.count() if Product.objects.count() > 0 else 0
        print_info(f"Average images per product: {avg_images:.1f}")

        return products_without_images == 0

    def verify_product_attributes(self):
        """Verify product attributes"""
        print_info("Verifying product attributes...")

        # Check product attributes
        attr_count = ProductAttribute.objects.count()
        print_info(f"Total product attributes: {attr_count}")

        # Check products without attributes
        products_without_attrs = Product.objects.filter(
            attributes__isnull=True
        ).count()

        if products_without_attrs == 0:
            print_success("All products have attributes")
            self.passed += 1
            return True
        else:
            print_warning(f"{products_without_attrs} products have no attributes")
            self.warnings += 1
            return True

    def verify_orders(self):
        """Verify order data"""
        print_info("Verifying order data...")

        order_count = Order.objects.count()
        print_info(f"Total orders: {order_count}")

        if order_count == 0:
            print_warning("No order data")
            self.warnings += 1
            return True

        # Verify order status distribution
        print_header("Order Status Distribution")
        status_dist = {
            'pending_payment': Order.objects.filter(status='pending_payment').count(),
            'pending_shipment': Order.objects.filter(status='pending_shipment').count(),
            'shipped': Order.objects.filter(status='shipped').count(),
            'completed': Order.objects.filter(status='completed').count(),
            'cancelled': Order.objects.filter(status='cancelled').count(),
        }

        has_distribution = False
        for status, count in status_dist.items():
            percentage = (count / order_count * 100) if order_count > 0 else 0
            print(f"  {status}: {count} ({percentage:.1f}%)")
            if count > 0:
                has_distribution = True

        if has_distribution:
            print_success("Order status distribution is reasonable")
            self.passed += 1
        else:
            print_warning("Order status distribution is limited")
            self.warnings += 1

        # Verify order items
        order_item_count = OrderItem.objects.count()
        print_info(f"Total order items: {order_item_count}")

        return True

    def verify_carts(self):
        """Verify cart data"""
        print_info("Verifying cart data...")

        cart_count = Cart.objects.count()
        cart_item_count = CartItem.objects.count()

        print_info(f"Carts: {cart_count}")
        print_info(f"Cart items: {cart_item_count}")

        return True

    def verify_coupons(self):
        """Verify coupon data"""
        print_info("Verifying coupon data...")

        coupon_count = Coupon.objects.count()
        user_coupon_count = UserCoupon.objects.count()

        print_info(f"Coupons: {coupon_count}")
        print_info(f"User coupons: {user_coupon_count}")

        if coupon_count >= 50:
            print_success(f"Coupon count is sufficient ({coupon_count} >= 50)")
            self.passed += 1
        else:
            print_warning(f"Coupon count is low ({coupon_count} < 50)")
            self.warnings += 1

        return True

    def verify_reviews(self):
        """Verify product reviews"""
        print_info("Verifying product reviews...")

        review_count = Review.objects.count()
        print_info(f"Product reviews: {review_count}")

        if review_count > 0:
            # Verify rating distribution
            avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg']
            print_info(f"Average rating: {avg_rating:.1f}/5" if avg_rating else "Average rating: N/A")

            # Check for invalid ratings
            invalid_ratings = Review.objects.filter(rating__lt=1).count() + Review.objects.filter(rating__gt=5).count()
            if invalid_ratings == 0:
                print_success("All ratings are valid (1-5)")
                self.passed += 1
            else:
                print_error(f"{invalid_ratings} invalid rating(s) found")
                self.failed += 1

        return True

    def verify_recommendations(self):
        """Verify recommendation data"""
        print_info("Verifying recommendation data...")

        rule_count = RecommendationRule.objects.count()
        recommended_product_count = RecommendedProduct.objects.count()

        print_info(f"Recommendation rules: {rule_count}")
        print_info(f"Recommended products: {recommended_product_count}")

        if rule_count >= 3:
            print_success(f"Recommendation rule count is sufficient ({rule_count} >= 3)")
            self.passed += 1
        else:
            print_warning(f"Recommendation rule count is low ({rule_count} < 3)")
            self.warnings += 1

        return True

    def verify_content(self):
        """Verify content data"""
        print_info("Verifying content data...")

        case_count = ModificationCase.objects.count()
        faq_count = FAQ.objects.count()

        print_info(f"Modification cases: {case_count}")
        print_info(f"FAQs: {faq_count}")

        all_valid = True

        if case_count >= 30:
            print_success(f"Modification case count is sufficient ({case_count} >= 30)")
            self.passed += 1
        else:
            print_warning(f"Modification case count is low ({case_count} < 30)")
            self.warnings += 1
            all_valid = False

        if faq_count >= 20:
            print_success(f"FAQ count is sufficient ({faq_count} >= 20)")
            self.passed += 1
        else:
            print_warning(f"FAQ count is low ({faq_count} < 20)")
            self.warnings += 1
            all_valid = False

        return all_valid

    def verify_system_data(self):
        """Verify system data"""
        print_info("Verifying system data...")

        config_count = SystemConfig.objects.count()
        message_count = Message.objects.count()
        log_count = OperationLog.objects.count()

        print_info(f"System configs: {config_count}")
        print_info(f"System messages: {message_count}")
        print_info(f"Operation logs: {log_count}")

        return True

    def verify_foreign_keys(self):
        """Verify foreign key constraints"""
        print_info("Verifying foreign key constraints...")

        try:
            # Test database foreign key integrity
            with connection.cursor() as cursor:
                # Check if product categories are valid
                invalid_categories = Product.objects.filter(
                    ~Q(category__in=Category.objects.all())
                ).count()

                # Check if order users are valid
                invalid_users = Order.objects.filter(
                    ~Q(user__in=User.objects.all())
                ).count()

                # Check if order item products are valid
                invalid_products = OrderItem.objects.filter(
                    ~Q(product__in=Product.objects.all())
                ).count()

                if invalid_categories == 0 and invalid_users == 0 and invalid_products == 0:
                    print_success("Foreign key constraints verified")
                    self.passed += 1
                    return True
                else:
                    print_error("Foreign key constraint verification failed")
                    if invalid_categories > 0:
                        print_error(f"  - {invalid_categories} products have invalid categories")
                    if invalid_users > 0:
                        print_error(f"  - {invalid_users} orders have invalid users")
                    if invalid_products > 0:
                        print_error(f"  - {invalid_products} order items have invalid products")
                    self.failed += 1
                    return False

        except Exception as e:
            print_error(f"Foreign key verification error: {e}")
            self.failed += 1
            return False

    def run_all(self):
        """Run all verifications"""
        print_header("Car Parts Sales Platform - Data Integrity Verification")

        # Execute verifications
        self.verify_user_count()
        self.verify_user_addresses()
        self.verify_categories()
        self.verify_products()
        self.verify_product_images()
        self.verify_product_attributes()
        self.verify_orders()
        self.verify_carts()
        self.verify_coupons()
        self.verify_reviews()
        self.verify_recommendations()
        self.verify_content()
        self.verify_system_data()
        self.verify_foreign_keys()

        # Print verification summary
        self.print_summary()

    def print_summary(self):
        """Print verification summary"""
        print_header("Verification Summary")

        total = self.passed + self.failed + self.warnings

        print(f"{Colors.BOLD}Passed:{Colors.RESET} {self.passed}")
        print(f"{Colors.BOLD}Failed:{Colors.RESET} {self.failed}")
        print(f"{Colors.BOLD}Warnings:{Colors.RESET} {self.warnings}")
        print(f"{Colors.BOLD}Total:{Colors.RESET} {total}")
        print()

        if self.failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}[PASS] All verifications passed! Data integrity is good.{Colors.RESET}\n")
            return 0
        else:
            print(f"{Colors.RED}{Colors.BOLD}[FAIL] {self.failed} verification(s) failed, please check the data!{Colors.RESET}\n")
            return 1


# ==================== Main Function ====================

def main():
    """Main function"""
    validator = DataValidator()
    return validator.run_all()


if __name__ == '__main__':
    exit(main())
