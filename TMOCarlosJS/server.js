const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3001;

// Define a route in your Express app
app.get('/', async (req, res) => {
  try {
    // Make a GET request to your Flask API endpoint
    const response = await axios.get('http://localhost:5000/');

    // Extract the data from the response
    const data = response.data;

    // Send the data to the client
    res.json(data);
  } catch (error) {
    // Handle errors
    console.error('Error fetching data from Flask API:', error.message);
    res.status(500).send('Internal Server Error');
  }
});

// Start the Express server
app.listen(PORT, () => {
  console.log(`Express server listening on port ${PORT}`);
});
