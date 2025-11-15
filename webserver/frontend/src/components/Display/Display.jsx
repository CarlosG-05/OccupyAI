import Card from '../Card/Card.jsx';

export default function Display(props) {
    console.log('levelInfo.data:', props.levelInfo && props.levelInfo.data);

    if (!props.levelInfo || !Array.isArray(props.levelInfo.data)) {
        return <div>Loading...</div>;
    }

    return (
        <>
            {props.levelInfo.data.map(room_info =>
                <Card
                    room_number={room_info.room_number}
                    current_occupancy={room_info.current_occupancy}
                    capacity={room_info.capacity}
                />
            )}
        </>
    );
}
