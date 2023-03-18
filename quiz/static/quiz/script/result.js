function removeBtnAni() {
    // const btnReset = document.getElementById("btn-reset");
    document.getElementById("btn-reset").classList.remove('rotated360');
}
document.getElementById("btn-reset").addEventListener('click', function () {
    document.getElementById("btn-reset").classList.add('rotated360');
    setTimeout(removeBtnAni, 500);
})