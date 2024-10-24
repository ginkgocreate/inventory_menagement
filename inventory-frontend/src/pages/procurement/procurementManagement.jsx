import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { TableContainer, Table, TableHead, TableRow, TableCell, TableBody, Paper, Button, Box, TextField } from '@mui/material';
import './procurementManagement.module.css';
import { postData } from 'utils/api';

const ProcurementManagement = () => {
const [procurements, setProcurements] = useState([]);

useEffect(() => {
    postData('/procurement/select')
    .then(response => setProcurements(response))
}, []);

const formatDate = (date) => {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');  // 月を2桁にする
    const day = String(d.getDate()).padStart(2, '0');  // 日を2桁にする
    return `${year}/${month}/${day}`;
};

return (
<Box sx={{ padding: 2 }}>
    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
    <TextField label="Search" variant="outlined" />
    <Link to="/procurement/register">
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
            <TableCell></TableCell>
            <TableCell>procurement_id</TableCell>
            <TableCell>procurement_seq</TableCell>
            <TableCell>platform_code</TableCell>
            <TableCell>purchase_date</TableCell>
            <TableCell>purchase_price</TableCell>
            <TableCell>shipping_fee</TableCell>
            <TableCell>supplier_id</TableCell>
            <TableCell>supplier_page_id</TableCell>
            <TableCell>supplier_url</TableCell>
            <TableCell>supplier_info</TableCell>
            <TableCell>category</TableCell>
            <TableCell>notes</TableCell>
            </TableRow>
        </TableHead>
        <TableBody>
            {procurements.map((procurement) => {
                return (
            <TableRow key={procurement.procurement_id}>
                <TableCell>
                <Link   
                    to="/stock/register"
                    state={{ procurement_id: procurement.procurement_id, procurement_seq: procurement.procurement_seq }}
                    style={{ textDecoration: 'none' }}
                    >
                    <Button 
                        variant="contained" 
                        color="primary"
                        style={{ width: '100px' }}>
                        在庫登録
                    </Button>
                </Link>
                </TableCell>
                <TableCell>
                <Link   
                    to="/procurement/register"
                    state={{ procurement_id: procurement.procurement_id, procurement_seq: procurement.procurement_seq }}
                    style={{ textDecoration: 'none' }}>
                    {procurement.procurement_id}
                    </Link>
                </TableCell>
                <TableCell>{procurement.procurement_seq}</TableCell>
                <TableCell>{procurement.platform_code}</TableCell>
                <TableCell>{procurement.purchase_date ? formatDate(procurement.purchase_date) : ''}</TableCell>
                <TableCell>{procurement.purchase_price}</TableCell>
                <TableCell>{procurement.shipping_fee}</TableCell>
                <TableCell>{procurement.supplier_id}</TableCell>
                <TableCell>{procurement.supplier_page_id}</TableCell>
                <TableCell>{procurement.supplier_url}</TableCell>
                <TableCell>{procurement.supplier_info}</TableCell>
                <TableCell>{procurement.category}</TableCell>
                <TableCell>{procurement.notes}</TableCell>
            </TableRow>
            );
        })}
        </TableBody>
        </Table>
    </TableContainer>
</Box>
);
};

export default ProcurementManagement;
