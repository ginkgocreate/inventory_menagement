import React, { useState, useEffect  } from 'react';
import { TextField, Button, Container, Typography, Box } from '@mui/material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { useLocation, useNavigate } from 'react-router-dom'; 
import { postData } from 'utils/api';

const StockForm = () => {
    const location = useLocation();
    const { procurement_id, procurement_seq, stock_id } = location.state || {};
    const [isStatusNew, setIsStatusNew] = useState(false);

    const [formData, setFormData] = useState({
        stock_id: stock_id || '',
        sales_id: '',
        category_id: '',
        asin: '',
        jan: '',
        manufacturer: '',
        product_name: '',
        model_number: '',
        serial_number: '',
        features: '',
        product_condition_notes: '',
        remarks: '',
    });

    useEffect(() => {
        if (procurement_id && procurement_seq && stock_id) {
            postData(`/stock/get-already`, {procurement_id: procurement_id, procurement_seq: procurement_seq, stock_id: stock_id})
                .then(response => {
                    setFormData(prevState => ({
                        ...prevState,
                        ...response,
                    }));
                })
                .catch(error => console.error('Error fetching procurement:', error));
        } else {
            setIsStatusNew(true);
            postData(`/stock/get-new`, {procurement_id: procurement_id, procurement_seq: procurement_seq, stock_id: stock_id})
                .then(response => {
                    setFormData(prevState => ({
                        ...prevState,
                        ...response,
                    }));
                })
                .catch(error => console.error('Error fetching procurement:', error));
        }
    }, [procurement_id, procurement_seq, stock_id]);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };
    
    const handleSubmit = (e) => {
        e.preventDefault();
        if (isStatusNew) {
            postData(`/stock/register`, formData)
            .then(response => {
                alert('stock updated successfully');
                handleBack();
            })
            .catch(error => {
                alert(`Error updating stock: ${error.response ? error.response.data.error : error.message}`);
                console.log(error.response)
            });
        } else {
            postData(`/stock/update`, formData)
            .then(response => {
                alert('stock updated successfully');
                handleBack();
            })
            .catch(error => {
                alert(`Error updating stock: ${error.response ? error.response.data.error : error.message}`);
                console.log(error.response)
            });
        }
        
    }
    const navigate = useNavigate(); 

    const handleBack = () => {
        navigate(-1);
    };

    return (
        <LocalizationProvider dateAdapter={AdapterDateFns}>
            <Container maxWidth="sm" sx={{ mt: 4, bgcolor: '#f9f9f9', p: 3, borderRadius: 2, boxShadow: 3 }}>
                <Typography variant="h4" align="center" gutterBottom>
                    在庫登録
                </Typography>
                <form onSubmit={handleSubmit}>
                    <TextField 
                        fullWidth 
                        inputProps={{ readOnly: true }}
                        label="在庫ID" 
                        name="stock_id" 
                        value={formData.stock_id} 
                        onChange={handleChange} 
                        required margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        inputProps={{ readOnly: true }}
                        label="販売ID" 
                        name="sales_id" 
                        value={formData.sales_id} 
                        onChange={handleChange} 
                        required margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="カテゴリ" 
                        name="category_id" 
                        value={formData.category_id} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="ASIN" 
                        name="asin" 
                        value={formData.asin} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="JAN" 
                        name="jan" 
                        value={formData.jan} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="メーカー" 
                        name="manufacturer" 
                        value={formData.manufacturer} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="商品名" 
                        name="product_name" 
                        value={formData.product_name} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="型番" 
                        name="model_number" 
                        value={formData.model_number} 
                        multiline 
                        rows={4} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="製造番号" 
                        name="serial_number" 
                        value={formData.serial_number} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="特徴・色など" 
                        name="features" 
                        value={formData.features} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="商品状態所見" 
                        name="product_condition_notes" 
                        value={formData.product_condition_notes} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <TextField 
                        fullWidth 
                        label="備考" 
                        name="remarks" 
                        value={formData.remarks} 
                        onChange={handleChange} 
                        margin="normal" 
                    />
                    <Box textAlign="center" sx={{ mt: 3, display: 'flex', justifyContent: 'center', gap: 2 }}>
                        <Button variant="contained" color="primary" type="submit">
                            {isStatusNew ? '新規登録' : '更新'}
                        </Button>
                        <Button variant="contained" color="secondary" onClick={handleBack}>
                            戻る
                        </Button>
                    </Box>
                </form>
            </Container>
        </LocalizationProvider>
    );
};

export default StockForm;
