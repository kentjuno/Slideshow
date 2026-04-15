// ==========================================
// CẤU HÌNH HIỆU ỨNG (Bạn có thể tự do thay đổi)
// ==========================================
// Chọn hiệu ứng bạn muốn: 'fireflies' (Con đom đóm), 'rain' (Mưa) hoặc 'snow' (Tuyết rơi)
const activeEffect = 'fireflies'; 

// Số lượng hạt (Mưa/Đom đóm...) trên màn hình
const particleDensity = 150; 


// ==========================================
// KHỞI TẠO KHUNG VẼ (CANVAS)
// ==========================================
const canvas = document.createElement('canvas');
document.body.appendChild(canvas);
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);


// ==========================================
// KIẾN TRÚC HIỆU ỨNG: ĐOM ĐÓM (FIREFLIES)
// ==========================================
class Firefly {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 1; // Kích thước ngẫu nhiên
        this.speedX = (Math.random() - 0.5) * 0.8;
        this.speedY = (Math.random() - 0.5) * 0.8;
        
        // Quỹ đạo lượn sóng cho tự nhiên
        this.angle = Math.random() * 360;
        this.angleSpeed = Math.random() * 0.02 - 0.01;
        
        // Độ nháy sáng
        this.brightness = Math.random();
        this.fading = Math.random() > 0.5;
        // Màu vàng tranh/nhạt của đóm đóm
        this.color = 'rgba(255, 240, 120, '; 
    }

    update() {
        // Di chuyển ngẫu nhiên kết hợp với lượn sóng
        this.angle += this.angleSpeed;
        this.x += this.speedX + Math.sin(this.angle) * 0.5;
        this.y += this.speedY + Math.cos(this.angle) * 0.5;

        // Nếu bay ra khỏi màn hình, cho xuất hiện lại ở bên kia
        if (this.x < 0) this.x = canvas.width;
        if (this.x > canvas.width) this.x = 0;
        if (this.y < 0) this.y = canvas.height;
        if (this.y > canvas.height) this.y = 0;

        // Tạo hiệu ứng tỏa sáng mờ ảo (nhấp nháy)
        if (this.fading) {
            this.brightness -= 0.01;
            if (this.brightness <= 0.1) this.fading = false;
        } else {
            this.brightness += 0.01;
            if (this.brightness >= 0.9) this.fading = true;
        }
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color + this.brightness + ")";
        
        // Tạo viền sáng mờ (Glow)
        ctx.shadowBlur = 15;
        ctx.shadowColor = "rgba(255, 240, 120, 0.8)";
        ctx.fill();
        ctx.shadowBlur = 0; // Tắt glow cho các nét vẽ khác
    }
}

// ==========================================
// KIẾN TRÚC HIỆU ỨNG: MƯA RƠI (RAIN)
// ==========================================
class Raindrop {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height - canvas.height;
        this.length = Math.random() * 20 + 20; // Độ dài hạt mưa
        this.speedY = Math.random() * 10 + 15; // Tốc độ rơi nhanh
        this.speedX = Math.random() * 1.5 - 0.75; // Sức gió nghiêng
    }

    update() {
        this.y += this.speedY;
        this.x += this.speedX;

        // Rơi chạm đáy -> Lên lại trên trời
        if (this.y > canvas.height) {
            this.y = -this.length;
            this.x = Math.random() * canvas.width;
            this.speedY = Math.random() * 10 + 15;
        }
    }

    draw() {
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(this.x + this.speedX, this.y + this.length);
        ctx.strokeStyle = "rgba(174, 194, 224, 0.7)"; // Màu mưa rơi (Trắng xám xanh)
        ctx.lineWidth = 1.5;
        ctx.lineCap = "round";
        ctx.stroke();
    }
}

// ==========================================
// KIẾN TRÚC HIỆU ỨNG: TUYẾT RƠI (SNOW)
// ==========================================
class Snowflake {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2.5 + 0.5;
        this.speedY = Math.random() * 1 + 0.5; // Tuyết rơi chậm
        this.angle = Math.random() * Math.PI * 2;
    }

    update() {
        this.y += this.speedY;
        // Tuyết lắc lư theo gió nhẹ
        this.x += Math.sin(this.angle) * 0.5;
        this.angle += 0.02;

        if (this.y > canvas.height) {
            this.y = -this.size;
            this.x = Math.random() * canvas.width;
        }
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(255, 255, 255, 0.8)"; // Trắng của tuyết
        ctx.fill();
    }
}


// ==========================================
// KHỞI CHẠY VÀ VẼ KHUNG HÌNH (ANIMATION LOOP)
// ==========================================
let particlesArray = [];

function initParticles() {
    particlesArray = [];
    for (let i = 0; i < particleDensity; i++) {
        if (activeEffect === 'fireflies') {
            particlesArray.push(new Firefly());
        } else if (activeEffect === 'rain') {
            particlesArray.push(new Raindrop());
        } else if (activeEffect === 'snow') {
            particlesArray.push(new Snowflake());
        }
    }
}

function animate() {
    // Để giữ lại nền trong suốt đè lên Slideshow OBS, ta dùng hàm clearRect
    // Hàm này sẽ lau sạch bản vẽ cũ để vẽ khung hình mới
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Di chuyển và hiển thị các hạt
    particlesArray.forEach(particle => {
        particle.update();
        particle.draw();
    });

    requestAnimationFrame(animate); 
}

// Chạy 
initParticles();
animate();
