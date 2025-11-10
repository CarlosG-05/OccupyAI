import './Header.css'

export default function Header() {
  return (
    <>
      <div class="container">
        <img class="title" src="/logo.png" alt="logo" width="200px" height="200px"/> 
        <h1>Love Library Study Rooms</h1>

        <div class="dropdown">
            <button class="dropbtn">Floor Level ᐯ</button>
            <div class="dropdown-content">
                <a href="#">Floor 1</a>
                <a href="#">Floor 2</a>
                <a href="#">Floor 3</a>
                <a href="#">Floor 4</a>
                <a href="#">Floor 5</a>
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

