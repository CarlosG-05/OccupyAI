import React, { useState, useEffect } from 'react';
import './App.css'
import Header from '../Header/Header.jsx'
import Banner from '../Banner/Banner.jsx'
import Display from '../Display/Display.jsx'

function App() {
    const [currentLevel, setCurrentLevel] = useState(1);
    const [levelInfo, setLevelInfo] = useState(null); 
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);           

    useEffect(() => {
        const fetchDataForLevel = async () => {
            setIsLoading(true); 
            setError(null);
            
            try {
                const url = `https://occupyai.onrender.com/floor/${currentLevel}`;
                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                console.log('Fetched data:', data);
                setLevelInfo(data); 

            } catch (err) {
                setError(err.message); 
            } finally {
                setIsLoading(false); 
            }
        };
        fetchDataForLevel();
    }, [currentLevel]); 
    
    return (
        <>
            <Header setCurrentLevel={setCurrentLevel} />
            <Banner level={currentLevel} />
            <h1>Room Availability</h1>
            <Display levelInfo={levelInfo} />
        </>
    );
}

export default App;
