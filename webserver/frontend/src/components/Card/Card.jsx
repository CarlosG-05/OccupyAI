import './Card.css';

export default function Card(props) {

    if (props.current_occupancy === 0) {
        return (
            <div className="card-container">
                <div className="card-info">
                    <h1>Room {props.room_number}</h1>
                    <h3>Occupancy: {props.current_occupancy}/{props.capacity}</h3>
                </div>
                <h1 className="room-state-occupied">Available</h1>
            </div>
        );
    }
    else {
        return (
            <div className="card-container">
                <div className="card-info">
                    <h1>Room {props.room_number}</h1>
                    <h3>Occupancy: {props.current_occupancy}/{props.capacity}</h3>
                </div>
                <h1 className="room-state-occupied">Occupied</h1>
            </div>
        );
    }
}
