# ระบบบริหารจัดการร้านปริ้นท์และงานเอกสารขนาดเล็ก
# แนวคิด: Make it Simple (ใช้งานผ่าน Console)

# ==========================================
# 1. Class สินค้า (Product)
# ==========================================
class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
    
    def display_info(self):
        # โชว์ข้อมูลสินค้า
        print(f"รหัส: {self.product_id} | {self.name} | ราคา: {self.price} บาท | คงเหลือ: {self.stock} ชิ้น")

    def update_stock(self, quantity):
        # ตรวจสอบและตัดสต็อก (กันสต็อกติดลบ)
        if quantity > 0 and quantity <= self.stock:
            self.stock -= quantity
            return True
        print("❌ สต็อกไม่พอ หรือใส่จำนวนผิด!")
        return False

# ==========================================
# 2. Class ลูกค้า (Customer)
# ==========================================
class Customer:
    def __init__(self, customer_id, name, contact, total_purchase=0.0):
        self.customer_id = customer_id
        self.name = name
        self.contact = contact
        self.total_purchase = total_purchase
    
    def display_customer(self):
        # โชว์ประวัติลูกค้า
        print(f"รหัส: {self.customer_id} | คุณ {self.name} | ยอดสะสม: {self.total_purchase} บาท")

    def record_purchase(self, amount):
        # บวกยอดเงินสะสมให้ลูกค้า
        if amount > 0:
            self.total_purchase += amount
            return True
        return False

# ==========================================
# 3. Class คำสั่งซื้อ (Order)
# ==========================================
class Order:
    def __init__(self, order_id, customer_name):
        self.order_id = order_id
        self.customer_name = customer_name
        self.cart_items = []    # ตะกร้าสินค้า
        self.total_amount = 0.0 # ราคารวม

    def add_item(self, product, quantity):
        # เอาของลงตะกร้า และตัดสต็อกทันที
        if product.update_stock(quantity): 
            subtotal = product.price * quantity
            # เก็บข้อมูลลงตะกร้า (เก็บตัว product ไว้ใช้ตอนยกเลิกด้วย)
            self.cart_items.append({"obj": product, "name": product.name, "qty": quantity, "subtotal": subtotal})
            self.total_amount += subtotal
            print(f"✅ เพิ่ม {product.name} ลงตะกร้าแล้ว")
            return True
        return False
        
    def print_receipt(self):
        # พิมพ์บิลใบเสร็จ
        print(f"\n=== ใบเสร็จ {self.order_id} | ลูกค้า: {self.customer_name} ===")
        for item in self.cart_items:
            print(f"- {item['name']} x {item['qty']} ชิ้น = {item['subtotal']} บาท")
        print(f"ยอดรวม: {self.total_amount} บาท\n=======================")

    def cancel_order(self):
        # คืนของเข้าสต็อก ล้างตะกร้า ล้างยอดเงิน
        for item in self.cart_items:
            item["obj"].stock += item["qty"] 
        self.cart_items = []
        self.total_amount = 0.0
        print(f"❌ ยกเลิกบิล {self.order_id} คืนสต็อกเรียบร้อย")

# ==========================================
# 4. เมนูหลัก (Main Menu)
# ==========================================
def main():
    # ข้อมูลสมมติตอนเปิดโปรแกรม
    products = [
        Product("P001", "ปริ้นท์ขาวดำ", 1.00, 500),
        Product("P002", "ปริ้นท์สี", 5.00, 250),
        Product("P003", "กระดาษแข็ง", 10.00, 100),
        Product("P004", "สันปกรายงาน", 5.00, 300)
    ]
    customers = [Customer("C001", "สมชาย", "081-111-1111")]
    orders_history = []
    order_id_run = 1

    while True:
        print("\n=== MINI SHOP SYSTEM ===")
        print("1. แสดงรายการสินค้า/บริการทั้งหมด")
        print("2. สร้างรายการสั่งซื้อ (ขายสินค้า)")
        print("3. ดูประวัติและยอดซื้อสะสมของลูกค้า")
        print("4. ยกเลิกบิลและคืนสต็อก")
        print("0. ออกจากโปรแกรม")
        print("="*24)
        choice = input("เลือกเมนู (0-4): ")

        if choice == "1":
            for p in products: p.display_info()

        elif choice == "2":
            # จำลองขายให้ลูกค้าคนแรกเสมอ (เพื่อให้ง่ายต่อการอธิบาย)
            cust = customers[0]
            #สร้างรหัสบิลใบเสร็จง่ายๆ
            new_order_id = f"Bill-{order_id_run}"
            #สร้างออบเจกต์คำสั่งซื้อใหม่ โดยส่งรหัสบิล และชื่อลูกค้าเข้าไป[cite: 4, 9]
            order = Order(new_order_id, cust.name)
            print(f"\n--- กำลังเปิดบิลให้ลูกค้า: คุณ {cust.name} ---")
            
            #ใช้ for loop พื้นฐาน เพื่อนับและแสดงรายการสินค้าทั้งหมดที่มี
            for i in range(len(products)):
                p = products[i] # ดึงสินค้าออกมาทีละชิ้น
                print(f"กดเลข [{i}] เลือก {p.name} (ราคา {p.price} บาท)")
                
            try:
                # ดักจับ Error กรณีผู้ใช้เผลอพิมพ์ตัวอักษรแทนตัวเลข[cite: 8]
                prod_idx = int(input("เลือกรหัสสินค้าตามเลขในวงเล็บ []: "))
                # ตรวจสอบว่าเลขที่พิมพ์มา อยู่ในรายการสินค้าที่มีหรือไม่
                if prod_idx >= 0 and prod_idx < len(products):
                    qty = int(input("รับกี่ชิ้น?: "))
                    # เปลี่ยนจากคำว่า INV เป็น Bill ให้เข้าใจง่ายขึ้น[cite: 10]
                    new_order_id = f"Bill-{order_id_run}"
                    # การดัก Error หากพิมพ์ตัวอักษรแทนตัวเลข
                    # เรียกใช้ Method จาก Class Order เพื่อนำสินค้าลงตะกร้า[cite: 4, 9]
                    if order.add_item(products[prod_idx], qty):
                        order.print_receipt()
                        cust.record_purchase(order.total_amount) # สะสมยอดให้ลูกค้า
                        orders_history.append(order)
                        order_id_run += 1 # บวกเลขบิลเพิ่มทีละ 1[cite: 10]
                else:
                    # การดักจับ Exception ป้องกันโปรแกรมพังเมื่อพิมพ์ตัวอักษรผิด[cite: 8]
                    print("-"*24)
                    print("❌ ขออภัยไม่มีสินค้านี้")
            except ValueError:
                # หากพิมพ์ตัวอักษร โค้ดจะตกลงมาที่นี่ และโปรแกรมจะไม่พัง[cite: 8]
                print("เกิดข้อผิดพลาด: ❌ กรุณาพิมพ์ตัวเลขเท่านั้น")
                

        elif choice == "3":
            for customer in customers: 
                customer.display_customer()

        elif choice == "4":
            if orders_history:
                # หยิบบิลใบล่าสุดออกจากตะกร้าประวัติ แล้วเก็บไว้ในตัวแปร last_order
                #.pop(): คือคำสั่ง (Method) พื้นฐานของข้อมูลประเภท List ใน Python ทำหน้าที่ "ดึงของชิ้นสุดท้ายออกจากกล่อง แล้วเอาของชิ้นนั้นมาให้เรา"
                #โดยให้ .pop()  ล้วงมือลงไปในกล่อง orders_history แล้วหยิบบิล "ใบล่าสุด (ใบที่อยู่ท้ายสุดของแถว)" ออกมา และลบบิลใบนั้นออกจากกล่องไปเลย
                last_order = orders_history.pop()
                # หักยอดเงินสะสมของลูกค้าคืน (อ้างอิงลูกค้าคนที่ 0)
                customers[0].total_purchase -= last_order.total_amount # หักยอดลูกค้าคืน
                # สั่งให้บิลใบนั้นยกเลิกตัวเอง (คืนของเข้าสต็อก)
                last_order.cancel_order() 
            else:
                print("❌ ไม่มีบิลให้ยกเลิก")

        elif choice == "0":
            print("ปิดโปรแกรม...")
            break
        else:
            print("❌ เลือกเมนูผิด")

if __name__ == "__main__":
    main()