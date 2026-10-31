import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const ReportDashboard = () => {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [reportData, setReportData] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    generateReport();
  }, []);

  const generateReport = async () => {
    setLoading(true);
    setError(null);

    const dateRange = `${startDate.toISOString().split('T')[0]} - ${endDate.toISOString().split('T')[0]}`;

    try {
      const response = await axios.get('/reports/product-performance', {
        params: {
          date_range: dateRange
        }
      });

      if (response.status === 200) {
        setReportData(response.data.report_data);
      }
    } catch (err) {
      console.error('Error generating report:', err);
      setError(err.message || 'Failed to generate report.');
      // Log error to server (replace with actual logging mechanism)
      console.warn('Reporting Error:', err);
      alert('Report generation failed. See console for details.'); 
    } finally {
      setLoading(false);
    }
  };

  const handleDateRangeChange = (start, end) => {
    setStartDate(start);
    setEndDate(end);
  };

  const formatReportData = () => {
    // Assuming report_data is an array of objects with product and sales
    return reportData.map(item => ({
      name: item.product,
      sales: item.sales
    }));
  };

  if (loading) {
    return <div>Loading report...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h2>Report Dashboard</h2>
      <DatePicker
        selected={startDate}
        endDate={endDate}
        onChange={handleDateRangeChange}
        startDate={startDate}
        endDate={endDate}
        inline
        calendarClassName="custom-datepicker"
      />
      <button onClick={generateReport}>Generate Report</button>

      {reportData.length > 0 && (
        <BarChart width={600} height={300} data={formatReportData()}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis dataKey="sales" />
          <Tooltip />
          <Legend />
          <Bar dataKey="sales" fill="#8884d8" />
        </BarChart>
      )}
    </div>
  );
};

export default ReportDashboard;