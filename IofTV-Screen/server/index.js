const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');

const app = express();
const PORT = process.env.PORT || 3000;

// Enable CORS for all routes
app.use(cors());
app.use(express.json());

// Water quality data endpoint
app.get('/api/water-quality', (req, res) => {
  try {
    const filePath = path.resolve(__dirname, '../../LightData/1-water_quality.csv');
    const fileContent = fs.readFileSync(filePath, 'utf8');
    
    // Parse CSV
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true
    });
    
    // Get the second row (index 1) or the latest data
    const latestData = records.length > 1 ? records[1] : records[0];
    
    return res.json({
      success: true,
      data: latestData
    });
  } catch (error) {
    console.error('Error reading water quality data:', error);
    return res.status(500).json({
      success: false,
      msg: 'Failed to read water quality data'
    });
  }
});

// Air quality data endpoint
app.get('/api/air-quality', (req, res) => {
  try {
    const filePath = path.resolve(__dirname, '../../LightData/2-air_quality.csv');
    const fileContent = fs.readFileSync(filePath, 'utf8');
    
    // Parse CSV
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true
    });
    
    // Get the second row (index 1) or the latest data
    const latestData = records.length > 1 ? records[1] : records[0];
    
    return res.json({
      success: true,
      data: latestData
    });
  } catch (error) {
    console.error('Error reading air quality data:', error);
    return res.status(500).json({
      success: false,
      msg: 'Failed to read air quality data'
    });
  }
});

// Water level data endpoint
app.get('/api/water-level', (req, res) => {
  try {
    const filePath = path.resolve(__dirname, '../../LightData/3-water_level.csv');
    const fileContent = fs.readFileSync(filePath, 'utf8');
    
    // Parse CSV
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true
    });
    
    // Get the second row (index 1) or the latest data
    const latestData = records.length > 1 ? records[1] : records[0];
    
    return res.json({
      success: true,
      data: latestData
    });
  } catch (error) {
    console.error('Error reading water level data:', error);
    return res.status(500).json({
      success: false,
      msg: 'Failed to read water level data'
    });
  }
});

// Hour West Lake data endpoint
app.get('/api/hour-west-lake', (req, res) => {
  try {
    const filePath = path.resolve(__dirname, '../../LightData/4-hour_wesk_lake.csv');
    const fileContent = fs.readFileSync(filePath, 'utf8');
    
    // Parse CSV - this file has a simpler format with Time,Value columns
    const records = parse(fileContent, {
      columns: false,
      skip_empty_lines: true
    });
    
    // Get the first 7 rows excluding header if any
    const header = records[0];
    const isHeader = isNaN(parseInt(header[1])); // Check if first row is header
    
    const startIndex = isHeader ? 1 : 0;
    const dataRows = records.slice(startIndex, startIndex + 7);
    
    // Format the data for chart display
    const chartData = dataRows.map(row => {
      // For hourly data, keep the full timestamp format
      return {
        time: row[0],
        value: parseInt(row[1])
      };
    });
    
    return res.json({
      success: true,
      data: chartData
    });
  } catch (error) {
    console.error('Error reading hour west lake data:', error);
    return res.status(500).json({
      success: false,
      msg: 'Failed to read hour west lake data'
    });
  }
});

// Day West Lake data endpoint
app.get('/api/day-west-lake', (req, res) => {
  try {
    const filePath = path.resolve(__dirname, '../../LightData/5-day_wesk_lake.csv');
    const fileContent = fs.readFileSync(filePath, 'utf8');
    
    // Parse CSV - this file has a simpler format with Time,Value columns
    const records = parse(fileContent, {
      columns: false,
      skip_empty_lines: true
    });
    
    // Get the first 7 rows excluding header if any
    const header = records[0];
    const isHeader = isNaN(parseInt(header[1])); // Check if first row is header
    
    const startIndex = isHeader ? 1 : 0;
    const dataRows = records.slice(startIndex, startIndex + 7);
    
    // Format the data for chart display - for daily data, just return the date
    const chartData = dataRows.map(row => {
      // For daily data, keep the full date format
      return {
        time: row[0],
        value: parseInt(row[1])
      };
    });
    
    return res.json({
      success: true,
      data: chartData
    });
  } catch (error) {
    console.error('Error reading day west lake data:', error);
    return res.status(500).json({
      success: false,
      msg: 'Failed to read day west lake data'
    });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
}); 