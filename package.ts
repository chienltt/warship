// 0. pkt_hello
export interface pkt_hello {
    type: 0,
    your_id: string,
    match_id: string,
    secretKey: string
}
//2. pkt_ok
export interface pkt_ok {
    type: 2
}
//3. pkt_place_ship
export interface coordinateOfShip {
    head:{x:number, y:number}
    tail:{x:number, y:number}
}
export interface pkt_place_ship {
    type:3,
    numberOfShip: number,
    coordinate: coordinateOfShip
}
//5. pkt_fire
export interface coordinateOfShot {
    x:number,
    y:number
}
export interface pkt_fire {
    type: 5,
    coordinate: coordinateOfShot
}

