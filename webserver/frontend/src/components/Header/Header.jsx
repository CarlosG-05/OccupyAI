import './Header.css'
import logo from '../../assets/logo.png';

export default function Header({ setCurrentLevel }) {
  return (
    <>
      <div className="container">
      <img className="title" src={logo} alt="logo" width="200px" height="200px"/> 
        <h1>Love Library Study Rooms</h1>

        <div className="dropdown">
            <button className="dropbtn">Floor Level ᐯ</button>
            <div className="dropdown-content">
                <a href="#" onClick={() => setCurrentLevel(1)}>Floor 1</a>
                <a href="#" onClick={() => setCurrentLevel(2)}>Floor 2</a>
                <a href="#" onClick={() => setCurrentLevel(3)}>Floor 3</a>
                <a href="#" onClick={() => setCurrentLevel(4)}>Floor 4</a>
                <a href="#" onClick={() => setCurrentLevel(5)}>Floor 5</a>
            </div>
        </div>

        <div class="dropdown" id="more">
            <button class="dropbtn">☰</button>
            <div class="dropdown-content">
                <a href="#">Contact</a>
                <a href="#">About</a>
            </div>
        </div>
      </div>
    </>
  )
}

