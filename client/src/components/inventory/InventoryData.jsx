import React, { useEffect, useState } from "react";
import { fetchData } from "../../api/inventoryApi";
import "./styles.scss";

const InventoryData = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getData = async () => {
    try {
      const inventoryData = await fetchData();
      setData(inventoryData);
      setLoading(false);
    } catch (err) {
      setError("Error fetching data, please try again.");
      setLoading(false);
    }
  };

  useEffect(() => {
    getData();
  }, []); 

  if (loading) return <div className="loading">Loading...</div>;

  if (error) return <div className="error">{error}</div>;

  return (
    <div className="inventory-container">
      <table className="inventory-table">
        <thead>
          <tr>
            <th>Item ID</th>
            <th>Movement</th>
            <th>Quantity</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {data.map(({ item_id, movement, quantity, timestamp }) => (
            <tr key={item_id}>
              <td>{item_id}</td>
              <td>{movement}</td>
              <td>{quantity}</td>
              <td>{new Date(timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default InventoryData;
