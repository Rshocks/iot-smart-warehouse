import React, { useEffect, useState } from 'react';
import { fetchData } from '../api/inventoryApi';

const InventoryData = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getData = async () => {
        try {
          const inventoryData = await fetchData();
          console.log('Fetched data:', inventoryData); // Log the response to the console
          setData(inventoryData);  // Set the data in state
          setLoading(false);
        } catch (error) {
          console.error("Error fetching data:", error);
          setLoading(false);
        }
      };
    getData();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="p-4 mt-6 border rounded-md shadow-md">
      <h2 className="text-xl mb-4">Inventory Data</h2>
      {data.length === 0 ? (
        <p>No data available.</p>
      ) : (
        <ul className="list-disc ml-4">
          {Array.isArray(data) &&
            data.map((item, index) => (
              <li key={index}>{JSON.stringify(item)}</li>
            ))}
        </ul>
      )}
    </div>
  );
};

export default InventoryData;
