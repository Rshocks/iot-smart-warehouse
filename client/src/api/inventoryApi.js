import axios from "axios";

const API_BASE_URL =  process.env.REACT_APP_API_BASE_URL;

export const fetchData = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/inventory`);
      const inventoryData = JSON.parse(response.data.body);
      return inventoryData;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
};
  