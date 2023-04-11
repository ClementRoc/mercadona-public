'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    rename = require('gulp-rename'),
    concat = require('gulp-concat'),
    autoprefixer = require('gulp-autoprefixer'),
    webp = require('gulp-webp');


var paths = {
    src: './static/',
    dest: './public/',
    imgDest: './public/img/',
    npm: 'node_modules/'
};

gulp.task('js', function () {
    return gulp.src(paths.src + 'js/**/*.*')
        .pipe(concat('app.js'))
        .pipe(gulp.dest(paths.dest + 'js'));
});

gulp.task('fonts', function() {
    return gulp.src(paths.src + 'fonts/*')
        .pipe(gulp.dest(paths.dest + 'fonts'));
});

gulp.task('css', function () {
    return gulp.src(paths.src + 'scss/app.scss')
        .pipe(sass())
        .pipe(autoprefixer({ browsers: ['last 2 versions'] }))
        .pipe(concat('app.css'))
        .pipe(gulp.dest(paths.dest + 'css'));
});

gulp.task('webp', function() {
    return gulp.src([paths.src + 'img/**/*.{jpg,jpeg,png}'])
        .pipe(rename({
            extname: '.webp',
        }))
        .pipe(webp({ quality: 80 }))
        .pipe(gulp.dest(paths.imgDest));
});

// Watch task
gulp.task('watch', function() {
    gulp.watch([paths.src + 'js/**/*.*'], gulp.series(['js']));
    gulp.watch([paths.src + 'scss/**/*.scss'], gulp.series(['css']));
});

// Force gulp watch to quit if user send a Ctrl + C
process.on('SIGINT', function() {
    process.exit();
});

exports.default = gulp.series(['css', 'js', 'webp', 'fonts'])


