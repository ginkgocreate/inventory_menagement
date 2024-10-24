import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/login/login';
import Menu from './pages/menu/menu';
import Stock from './pages/stock/stockManagement';
import StockRegister from './pages/stock/stockRegister';
import Procurement from './pages/procurement/procurementManagement';
import ProcurementRegister from './pages/procurement/procurementRegister';
import Sales from './pages/sales/salesManagement';
import SalesRegister from './pages/sales/salesRegister';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/menu" element={<Menu />} />
                <Route path="/stock" element={<Stock />} />
                <Route path="/stock/register" element={<StockRegister />} />
                <Route path="/procurement" element={<Procurement />}/>
                <Route path="/procurement/register" element={<ProcurementRegister />}/>
                <Route path="/sales" element={<Sales />}/>
                <Route path="/sales/register/" element={<SalesRegister />}/>
            </Routes>
        </Router>
    );
};

export default App;
