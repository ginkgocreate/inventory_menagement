import React, { useState, useEffect  } from 'react';
import { TextField, Button, Container, Typography, Box, TableContainer, Table, TableHead, TableRow, TableCell, TableBody, Paper } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { useLocation, useNavigate, Link } from 'react-router-dom'; 
import { postData } from 'utils/api';

const ProcurementForm = () => {
    const location = useLocation();
    const { procurement_id, procurement_seq } = location.state || {};

    const [formData, setFormData] = useState({
        procurement_seq: '',
        platform_code: '',
        purchase_date: '',
        purchase_price: '',
        shipping_fee: '',
        supplier_id: '',
        supplier_page_id: '',
        supplier_url: '',
        supplier_info: '',
        category: '',
        notes: '',
    });

    const [stocks, setStocks] = useState([]); 

    useEffect(() => {
        if (procurement_id) {
            console.log(procurement_id, procurement_seq)
            postData(`/procurement/get`, {procurement_id: procurement_id, procurement_seq: procurement_seq})
                .then(response => {
                    setFormData({
                        ...response,
                        purchase_date: new Date(response.purchase_date)
                    });
                })
                .catch(error => console.error('Error fetching procurement:', error));
        
         // stock データの取得
        if (procurement_id && procurement_seq) {
            postData('/stock/get-stock-list', {procurement_id: procurement_id, procurement_seq: procurement_seq})
                .then(response => {
                    console.log('Stock data:', response);
                    setStocks(response);  // stock一覧をセット
                })
                .catch(error => console.error('Error fetching stocks:', error));
            }
        }
    }, [procurement_id, procurement_seq]);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };
    
    const handleDateChange = (newDate) => {
        setFormData({
            ...formData,
            purchase_date: newDate
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (procurement_id) {
            postData(`/procurement/register`, formData)
                .then(response => {
                    alert('Procurement updated successfully');
                    handleBack();
                })
                .catch(error => {
                    alert(`Error updating procurement: ${error.response ? error.response.data.error : error.message}`);
                });
        } else {
            postData('/procurement/register', formData)
            .then(response => {
                alert('Procurement added successfully');
                handleBack();
            })
            .catch(error => {
                alert(`Error fetching procurements: ${error.response ? error.response.data.error : error.message}`);
                console.log(error.response.data.error)
            });    
        };
    }
    const navigate = useNavigate(); 

    const handleBack = () => {
        navigate(-1);
    };

    return (
        <LocalizationProvider dateAdapter={AdapterDateFns}>
            <Container maxWidth="sm" sx={{ mt: 4, bgcolor: '#f9f9f9', p: 3, borderRadius: 2, boxShadow: 3 }}>
                <Typography variant="h4" align="center" gutterBottom>
                    仕入れ登録
                </Typography>
                <form onSubmit={handleSubmit}>
                    <TextField fullWidth label="プラットフォーム" name="platform_code" value={formData.platform_code} onChange={handleChange} required margin="normal" />
                    <DatePicker
                        label="仕入日"
                        value={formData.purchase_date}
                        onChange={handleDateChange}
                        renderInput={(params) => <TextField fullWidth margin="normal" {...params} />}
                    />
                    <TextField 
                        fullWidth label="仕入れ価格" 
                        name="purchase_price" 
                        value={formData.purchase_price} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="送料" 
                        name="shipping_fee" 
                        value={formData.shipping_fee} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="仕入れ元ID" 
                        name="supplier_id" 
                        value={formData.supplier_id} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="仕入れ元ページID" 
                        name="supplier_page_id" 
                        value={formData.supplier_page_id} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="仕入れ元URL" 
                        name="supplier_url" 
                        value={formData.supplier_url} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="仕入れ元情報" 
                        name="supplier_info" 
                        value={formData.supplier_info} 
                        multiline 
                        rows={4} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="カテゴリ" 
                        name="category" 
                        value={formData.category} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="備考" 
                        name="notes" 
                        value={formData.notes} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                </form>
                 {/* stock一覧表示部分 */}
                <Box mt={4}>
                    <Typography variant="h5" align="center" gutterBottom>
                        在庫一覧
                    </Typography>
                    <Link   
                    to="/stock/register"
                    state={{ procurement_id: procurement_id, procurement_seq: procurement_seq }}
                    style={{ textDecoration: 'none' }}
                    >
                    <Button 
                        variant="contained" 
                        color="primary"
                        style={{ width: '100px' }}>
                        在庫登録
                    </Button>
                    </Link>
                    <TableContainer component={Paper}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>在庫ID</TableCell>
                                    <TableCell>ASIN</TableCell>
                                    <TableCell>JAN</TableCell>
                                    <TableCell>メーカー</TableCell>
                                    <TableCell>商品名</TableCell>
                                    <TableCell>型番</TableCell>
                                    <TableCell>製造番号</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {stocks.map((stock) => (
                                    <TableRow key={stock.stock_id}>
                                        <TableCell>
                                            <Link   
                                                to="/stock/register"
                                                state={{ procurement_id: procurement_id, procurement_seq: procurement_seq, stock_id: stock.stock_id }}
                                                style={{ textDecoration: 'none' }}
                                                >
                                                <Button 
                                                    variant="contained" 
                                                    color="primary"
                                                    style={{ width: '50px' }}>
                                                    {stock.stock_id}
                                                </Button>
                                            </Link>
                                        </TableCell>
                                        <TableCell>{stock.asin}</TableCell>
                                        <TableCell>{stock.jan}</TableCell>
                                        <TableCell>{stock.manufacturer}</TableCell>
                                        <TableCell>{stock.product_name}</TableCell>
                                        <TableCell>{stock.model_number}</TableCell>
                                        <TableCell>{stock.serial_number}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Box>
                <Box textAlign="center" sx={{ mt: 3, display: 'flex', justifyContent: 'center', gap: 2 }}>
                    <Button variant="contained" color="primary" type="submit">
                        Add Procurement
                    </Button>
                    <Button variant="contained" color="secondary" onClick={handleBack}>
                        Back Previous
                    </Button>
                </Box>
            </Container>
        </LocalizationProvider>
    );
};

export default ProcurementForm;
