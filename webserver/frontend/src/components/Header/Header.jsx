import './Header.css'

export default function Header({ setCurrentLevel }) {

    return (
      <>
        <div class="container">
          <img class="title" src="/logo.png" alt="logo" width="200px" height="200px"/> 
          <h1>Love Library Study Rooms</h1>

          <div class="dropdown">
              <button class="dropbtn">Floor Level ᐯ</button>
              <div class="dropdown-content">
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
