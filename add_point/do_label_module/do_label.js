let index = -1;




/////// not available for safary
/////// please use chrome


/// config
const root_path = "../temp/";
const MAX_POINT = 5;
const MY_LINK = [[0,1],[1,2],[2,3],[3,4]];
const API_PATH = 'https://favorite-innocent-design.anvil.app/_/api/dme';

/// css
const border_size = 10;
const line_color = 'white';
const point_size = 3;
const point_color = 'red';
const point_border = 'black';


///
const output_p = $('#output_p')[0];
const canvas_canvas = $('#canvas_canvas')[0];
let ctx = canvas_canvas.getContext('2d');
let point_collection = [];

async function show_img(index) {
    output_p.innerHTML = "index = " + index;
    let img_path = root_path + '/' + index + '.jpg';
    function loadImage(url) {
        return new Promise(r => { let i = new Image(); i.onload = (() => r(i)); i.src = url; });
    }
    let img = await loadImage(img_path);
    ctx.drawImage(img, 0, 0, canvas_canvas.width, canvas_canvas.height);
}
$('#previous_btn').click(() => {
    index -= 1;
    show_img(index);
});
$('#next_btn').click(() => {
    index += 1;
    show_img(index);
});
$('#save_btn').click(() => {
    index += 1;
    show_img(index);
    // save points

    point_collection = [];
});
$('#canvas_canvas').mousedown(async (e) => {
    function getCoordinates(e) {
        let x = e.clientX - canvas_canvas.offsetLeft - border_size - 1;
        let y = e.clientY - canvas_canvas.offsetTop - border_size - 2;
        let point = [x, y];
        $('#x').html(x);
        $('#y').html(y);
        return point;
    }
    let point = getCoordinates(e);
    if (point_collection.length < MAX_POINT){
        point_collection.push(point);
        await handle_points(point_collection);
    }else{
        alert('too much point?');

    }
})

document.addEventListener('keypress', async function (e) {
    // 13 -> enter button
    // 32 -> space button
    // 59 -> ;
    e.preventDefault();
    console.log(index);
    if (e.which == 32 ) {
        // dat
        //// four point
        // save

        if (point_collection.length != MAX_POINT){
            alert('n point_collection != max_point');
        }else{
            function toStr(point){
                return point[0]/600 + ',' + point[1]/600 + ';'
            }
            // save
            let dat = '';
            point_collection.forEach((point)=>{
                dat += toStr(point);
            })
            point_collection = [];
            await do_api(index, dat);
            index += 1;
            show_img(index);
        }
    }
});



async function do_api(index, dat){
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
    "i": index,
    "dat": dat
    });

    var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
    };

    fetch("https://favorite-innocent-design.anvil.app/_/api/dme", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
}

function draw_display(_points){
    // draw points
    _points.forEach((p) => draw_point(p))

    // draw link
    MY_LINK.forEach(
        (val) => {
            if (val) {
                let a = val[0];
                let b = val[1];
                console.log('--------');
                console.log(a);
                console.log(b);
                console.log(_points.length);
                console.log(_points[a]);
                console.log('---end-----');

                if (_points.length > a && _points.length > b){
                    draw_line(_points[a], _points[b]);
                }

            }
        } 
    );
}

/// draw function
async function handle_points(_points) {
    if (_points.length < MAX_POINT) {
        await show_img(index);
        
        draw_display(_points);
    }
    else if (_points.length == MAX_POINT) {
        draw_display(_points);
        
    }
    else{
        alert('xxx');
    }
    console.log(point_collection);
}

async function draw_rect(_points) {
    if (_points.length == 1) {
        // clear draw
        // await show_img(index)
        alert('hellllll');
    }
    else if (_points.length == 2) {
        // draw rect
        let p0 = _points[0];
        let p1 = _points[1];
        // let vector = [p1[0] - p0[0], p1[1] - p0[1]];
        // rotate vector
        function rotate(cx, cy, x, y, angle) {
            var radians = (Math.PI / 180) * angle,
                cos = Math.cos(radians),
                sin = Math.sin(radians),
                nx = (cos * (x - cx)) + (sin * (y - cy)) + cx,
                ny = (cos * (y - cy)) - (sin * (x - cx)) + cy;
            return [nx, ny];
        }
        let r90 = rotate(p0[0], p0[1], p1[0], p1[1], 90);
        let r180 = rotate(p0[0], p0[1], p1[0], p1[1], 180);
        let r270 = rotate(p0[0], p0[1], p1[0], p1[1], 270);
        draw_point(r90);
        draw_point(r180);
        draw_point(r270);
        draw_line(p0, p1);
        draw_line(p0, r90);
        draw_line(p0, r180);
        draw_line(p0, r270);
        draw_line(p1, r270);
        draw_line(p1, r90);
        draw_line(r90, r180);
        draw_line(r180, r270);
        point_collection = [];
    }
    console.log(point_collection);
    _points.forEach((p) => {
        draw_point(p)
    })
}

function draw_line(p0, p1) {
    ctx.strokeStyle = line_color;
    ctx.beginPath();
    ctx.moveTo(p0[0], p0[1]);
    ctx.lineTo(p1[0], p1[1]);
    ctx.stroke();
}

function draw_point(p) {
    ctx.fillStyle = point_color;
    ctx.strokeStyle = point_border;
    ctx.beginPath();
    ctx.arc(p[0], p[1], point_size, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
}

function sqr(x) {
    return x * x;
}

function dist2(v, w) {
    return sqr(v[0] - w[0]) + sqr(v[1] - w[1]);
}

function distToSegmentSquared(p, v, w) {
    // p - point
    // v - start point of segment
    // w - end point of segment
    var l2 = dist2(v, w);
    if (l2 === 0) return dist2(p, v);
    var t = ((p[0] - v[0]) * (w[0] - v[0]) + (p[1] - v[1]) * (w[1] - v[1])) / l2;
    t = Math.max(0, Math.min(1, t));
    return dist2(p, [v[0] + t * (w[0] - v[0]), v[1] + t * (w[1] - v[1])]);
}

function distToSegment(p, v, w) {
    // p - point
    // v - start point of segment
    // w - end point of segment
    return Math.sqrt(distToSegmentSquared(p, v, w));
}

function rotate(cx, cy, x, y, angle) {
    var radians = (Math.PI / 180) * angle,
        cos = Math.cos(radians),
        sin = Math.sin(radians),
        nx = (cos * (x - cx)) + (sin * (y - cy)) + cx,
        ny = (cos * (y - cy)) - (sin * (x - cx)) + cy;
    return [nx, ny];
}

function extend_vec(p0, p1, dist) {
    let vec_size = ((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2) ** 0.5
    let vec = [p1[0] - p0[0], p1[1] - p0[1]]
    let unit_vec = [vec[0] / vec_size, vec[1] / vec_size]
    let extended_point = [p0[0] + unit_vec[0] * dist, p0[1] + unit_vec[1] * dist]
    return extended_point
}