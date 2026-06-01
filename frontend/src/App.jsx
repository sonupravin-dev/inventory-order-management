import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const API = "https://inventory-order-management-1-hhhm.onrender.com";

  // PRODUCTS
  const [products, setProducts] = useState([]);
  const [name, setName] = useState("");
  const [sku, setSku] = useState("");
  const [price, setPrice] = useState("");
  const [stock, setStock] = useState("");

  // CUSTOMERS
  const [customers, setCustomers] = useState([]);
  const [cName, setCName] = useState("");
  const [cEmail, setCEmail] = useState("");
  const [cPhone, setCPhone] = useState("");

  // ORDERS
  const [orders, setOrders] = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState("");
  const [selectedProduct, setSelectedProduct] = useState("");
  const [quantity, setQuantity] = useState("");

  // FETCH PRODUCTS
  const fetchProducts = () => {
    axios.get(`${API}/products`)
      .then(res => setProducts(res.data));
  };

  // FETCH CUSTOMERS
  const fetchCustomers = () => {
    axios.get(`${API}/customers`)
      .then(res => setCustomers(res.data));
  };

  // FETCH ORDERS
  const fetchOrders = () => {
    axios.get(`${API}/orders`)
      .then(res => setOrders(res.data));
  };

  useEffect(() => {
    fetchProducts();
    fetchCustomers();
    fetchOrders();
  }, []);

  // ADD PRODUCT
  const addProduct = () => {
    axios.post(`${API}/products`, {
      name,
      sku,
      price: parseFloat(price),
      stock_quantity: parseInt(stock)
    }).then(() => {
      fetchProducts();
      setName("");
      setSku("");
      setPrice("");
      setStock("");
    });
  };

  // ADD CUSTOMER
  const addCustomer = () => {
    axios.post(`${API}/customers`, {
      name: cName,
      email: cEmail,
      phone: cPhone
    }).then(() => {
      fetchCustomers();
      setCName("");
      setCEmail("");
      setCPhone("");
    });
  };

  // CREATE ORDER
  const createOrder = () => {
  if (!selectedCustomer || !selectedProduct || !quantity) {
    alert("Please select customer, product and quantity");
    return;
  }

  axios.post(`${API}/orders`, {
    customer_id: parseInt(selectedCustomer),
    items: [
      {
        product_id: parseInt(selectedProduct),
        quantity: parseInt(quantity)
      }
    ]
  })
  .then(() => {
    fetchOrders();
    fetchProducts();
  })
  .catch((err) => {
    console.log(err);
    alert("Order failed. Check console");
  });
};
  return (
    <div style={{ padding: "20px" }}>
      <h1>Inventory System</h1>

      {/* PRODUCTS */}
      <h2>Add Product</h2>
      <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
      <input placeholder="SKU" value={sku} onChange={e => setSku(e.target.value)} />
      <input placeholder="Price" value={price} onChange={e => setPrice(e.target.value)} />
      <input placeholder="Stock" value={stock} onChange={e => setStock(e.target.value)} />
      <button onClick={addProduct}>Add Product</button>

      <h2>Products</h2>
      {products.map(p => (
        <div key={p.id}>
          {p.name} - ₹{p.price} - Stock: {p.stock_quantity}
        </div>
      ))}

      <hr />

      {/* CUSTOMERS */}
      <h2>Add Customer</h2>
      <input placeholder="Name" value={cName} onChange={e => setCName(e.target.value)} />
      <input placeholder="Email" value={cEmail} onChange={e => setCEmail(e.target.value)} />
      <input placeholder="Phone" value={cPhone} onChange={e => setCPhone(e.target.value)} />
      <button onClick={addCustomer}>Add Customer</button>

      <h2>Customers</h2>
      {customers.map(c => (
        <div key={c.id}>
          {c.name} - {c.email} - {c.phone}
        </div>
      ))}

      <hr />

      {/* ORDERS */}
      <h2>Create Order</h2>

      <select onChange={e => setSelectedCustomer(e.target.value)}>
        <option value="">Select Customer</option>
        {customers.map(c => (
          <option value={c.id} key={c.id}>
            {c.name}
          </option>
        ))}
      </select>

      <select onChange={e => setSelectedProduct(e.target.value)}>
        <option value="">Select Product</option>
        {products.map(p => (
          <option value={p.id} key={p.id}>
            {p.name}
          </option>
        ))}
      </select>

      <input
        placeholder="Quantity"
        value={quantity}
        onChange={e => setQuantity(e.target.value)}
      />

      <button onClick={createOrder}>Place Order</button>

      <h2>Orders</h2>
      {orders.map(o => (
        <div key={o.order_id}>
          <p>Order ID: {o.order_id}</p>
          <p>Customer: {o.customer_name}</p>
          <p>Total: ₹{o.total_amount}</p>
        </div>
      ))}
    </div>
  );
}

export default App;