import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { TableContainer, Table, TableHead, TableRow, TableCell, TableBody, Paper, Button, Box, TextField } from '@mui/material';
import { postData } from 'utils/api';

const StockManagement = () => {
const [stocks, setStock] = useState([]);
const location = useLocation();
const params = new URLSearchParams(location.search);
const procurement_id = params.get('procurement_id');
const seq = params.get('seq');

useEffect(() => {
    postData('/stock/select')
    .then(response => setStock(response))
}, []);

return (
<Box sx={{ padding: 2 }}>
    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
    <TextField label="Search" variant="outlined" />
    <Link to="/stock/register">
        <Button variant="contained" color="primary">
        New Procurement
        </Button>
    </Link>
    </Box>

    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
    <Link to="/menu">
        <Button variant="contained" color="primary">
        Menu
        </Button>
    </Link>
    </Box>

    <TableContainer component={Paper}>
        <Table aria-label="procurement table">
        <TableHead>
            <TableRow>
            <TableCell>在庫ID</TableCell>
            <TableCell>販売ID</TableCell>
            <TableCell>カテゴリ</TableCell>
            <TableCell>ASIN</TableCell>
            <TableCell>JAN</TableCell>
            <TableCell>メーカー</TableCell>
            <TableCell>商品名</TableCell>
            <TableCell>型番</TableCell>
            <TableCell>製造番号</TableCell>
            <TableCell>特徴</TableCell>
            <TableCell>コンディション所見</TableCell>
            <TableCell>備考</TableCell>
            </TableRow>
        </TableHead>
        <TableBody>
            {stocks.map((stock) => {
                return (
            <TableRow key={stock.procurement_id}>
                <TableCell>
                <Link   
                    to="/stock/register"
                    state={{ procurement_id: stock.procurement_id, procurement_seq: stock.procurement_seq, stock_id: stock.stock_id }}
                    style={{ textDecoration: 'none' }}>
                    {stock.procurement_id}-{stock.procurement_seq}-{stock.stock_id}
                    </Link>
                </TableCell>
                <TableCell>{stock.sales_id}</TableCell>
                <TableCell>{stock.category_id}</TableCell>
                <TableCell>{stock.asin}</TableCell>
                <TableCell>{stock.jan}</TableCell>
                <TableCell>{stock.manufacturer}</TableCell>
                <TableCell>{stock.product_name}</TableCell>
                <TableCell>{stock.model_number}</TableCell>
                <TableCell>{stock.serial_number}</TableCell>
                <TableCell>{stock.features}</TableCell>
                <TableCell>{stock.product_condition_notes}</TableCell>
                <TableCell>{stock.remarks}</TableCell>
            </TableRow>
            );
        })}
        </TableBody>
        </Table>
    </TableContainer>
</Box>
);
};

export default StockManagement;
