import React, { useEffect, useState } from "react";
import { fetchData } from "../../api/inventoryApi";
import Pagination from "../../components/Pagination";
import "./styles.scss";

const InventoryData = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Pagination State
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  useEffect(() => {
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
    getData();
  }, []);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  const totalPages = Math.ceil(data.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentItems = data.slice(startIndex, startIndex + itemsPerPage);

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
          {currentItems.map(({ item_id, movement, quantity, timestamp }) => (
            <tr key={item_id}>
              <td>{item_id}</td>
              <td>{movement}</td>
              <td>{quantity}</td>
              <td>{new Date(timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <Pagination 
        currentPage={currentPage} 
        totalPages={totalPages} 
        onPageChange={setCurrentPage} 
      />
    </div>
  );
};

export default InventoryData;
