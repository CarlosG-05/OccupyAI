import './Banner.css'

export default function Banner(props) {
    return (
        <div class="banner-container">
            <img src="/banner-love-library.jpg" alt="banner" width="100%" height="100%" />
            <h1 class="overlay-text">Floor Level {props.level}</h1>
        </div>);
}
