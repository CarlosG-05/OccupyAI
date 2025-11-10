import React, { useState } from 'react';
import './App.css'
import Header from '../Header/Header.jsx'
import Banner from '../Banner/Banner.jsx'

function App() {
    const [currentLevel, setCurrentLevel] = useState(1);

    return (
        <>
            <Header setCurrentLevel={setCurrentLevel} />
            <Banner level={currentLevel} />
        </>
    );
}

export default App
