document.addEventListener('DOMContentLoaded', () => {
    console.log('Chungwan Website Loaded');

    // --- Hero Text Rotator ---
    const rotatingSubtitle = document.getElementById('hero-rotating-subtitle');
    if (rotatingSubtitle) {
        const subtitles = [
            "청완은 우리 삶의 질을 높이기 위해 최선을 다 합니다.",
            "Amenity - Safety - Sustainability<br><small>공동주택을 쾌적하게, 안전하게, 쉽게 유지보수 할 수 있는 제품을 개발 합니다.</small>",
            "DUBS - Fire Block - Sleeve Sextia Drain<br><small>욕실 층간소음 냄새 없는 층상이중배관, 화재로부터 안전한 층간방화재, 각종 배수 배관자재를 만듭니다.</small>"
        ];
        let subIndex = 0;

        setInterval(() => {
            // Fade out
            rotatingSubtitle.classList.add('hidden');

            setTimeout(() => {
                // Change text
                subIndex = (subIndex + 1) % subtitles.length;
                rotatingSubtitle.innerHTML = subtitles[subIndex];
                
                // Fade in
                rotatingSubtitle.classList.remove('hidden');
            }, 500); // Wait for fade out

        }, 4000); // 4 seconds total cycle
    }


    // --- Certificate Modal Functionality ---
    const certItems = document.querySelectorAll('.cert-item img'); // Select images directly
    
    // Create Modal Elements
    const modal = document.createElement('div');
    modal.id = 'cert-modal';
    Object.assign(modal.style, {
        display: 'none',
        position: 'fixed',
        zIndex: '2000',
        left: '0',
        top: '0',
        width: '100%',
        height: '100%',
        overflow: 'hidden', /* Prevent scrolling underlying body */
        backgroundColor: 'rgba(0,0,0,0.9)',
        flexDirection: 'column', /* Stack image and caption vertically */
        alignItems: 'center',
        justifyContent: 'center',
        backdropFilter: 'blur(5px)'
    });

    const modalImg = document.createElement('img');
    modalImg.id = 'img01';
    Object.assign(modalImg.style, {
        display: 'block',
        maxWidth: '80%',
        maxHeight: '80%',
        width: 'auto', /* Allow scaling */
        height: 'auto',
        objectFit: 'contain',
        boxShadow: '0 0 20px rgba(0,0,0,0.5)',
        borderRadius: '8px',
        margin: '0 auto' /* Reset margin to rely on flex centering */
    });

    const closeBtn = document.createElement('span');
    closeBtn.innerHTML = '&times;';
    Object.assign(closeBtn.style, {
        position: 'absolute',
        top: '15px',
        right: '35px',
        color: '#f1f1f1',
        fontSize: '40px',
        fontWeight: 'bold',
        transition: '0.3s',
        cursor: 'pointer',
        zIndex: '2001'
    });

    const captionText = document.createElement('div');
    Object.assign(captionText.style, {
        margin: '20px auto 0',
        display: 'block',
        width: 'auto',
        maxWidth: '80%',
        textAlign: 'center',
        color: '#ccc',
        fontSize: '18px',
        fontWeight: '500'
    });

    modal.appendChild(closeBtn);
    modal.appendChild(modalImg);
    modal.appendChild(captionText);
    document.body.appendChild(modal);

    // Event Listeners
    certItems.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            modal.style.display = 'flex'; // Important: set to flex to activate centering
            modalImg.src = this.src;
            captionText.innerHTML = this.alt;
        });
    });

    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }

    modal.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    }
});
