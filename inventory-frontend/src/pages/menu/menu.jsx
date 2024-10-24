import React from 'react';
import { Link } from 'react-router-dom';
import styles from './menu.module.css';

const Menu = () => {
    return (
        <div className={styles.container}>
            <h2>MENU</h2>
            <Link to="/stock" className={styles.link}>在庫管理</Link>
            <br />
            <Link to="/procurement" className={styles.link}>仕入れ管理</Link>
            <br />
            <Link to="/sales" className={styles.link}>販売管理</Link>
        </div>
    );
};

export default Menu;