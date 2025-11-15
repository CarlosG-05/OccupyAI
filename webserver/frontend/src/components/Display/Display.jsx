import Card from '../Card/Card.jsx';


export default function Display(props) {
    if (!props.levelInfo || !props.levelInfo.data) {
        return <div>Loading rooms...</div>;
    }

    return (
        <>
            {props.levelInfo.data.map(room_info => (
                <Card
                    key={room_info.room_number}
                    room_number={room_info.room_number}
                    current_occupancy={room_info.current_occupancy}
                    capacity={room_info.capacity}
                />
            ))}
        </>
    );
}
