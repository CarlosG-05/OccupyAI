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
                const url = `https://jsonplaceholder.typicode.com/posts/${currentLevel}`;
                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                
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
            <Display />

            <div style={{ padding: '20px' }}>
                <hr />
                <h2>API Response for Post #{currentLevel}:</h2>

                {isLoading && <p>Loading...</p>}

                {error && <p style={{ color: 'red' }}>Error: {error}</p>}

                {levelInfo && (
                    <article>
                        <h3>Title: {levelInfo.title}</h3>
                        <p>Body: {levelInfo.body}</p>
                        <small>User ID: {levelInfo.userId}</small>
                    </article>
                )}
            </div>
        </>
    );
}

export default App;
