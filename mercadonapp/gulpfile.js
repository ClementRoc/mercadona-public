'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass')(require('sass')),
    rename = require('gulp-rename'),
    plumber = require('gulp-plumber'),
    gutil = require('gulp-util'),
    cleanCSS = require('gulp-clean-css'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat'),
    autoprefixer = require('gulp-autoprefixer'),
    webp = require('gulp-webp');

var paths = {
    src: './assets/',
    dest: './static/',
    imgDest: './static/img/',
    npm: 'node_modules/'
};

var minifyIfNeeded = function (alwaysMinify) {
    return alwaysMinify === true || gutil.env.env === 'prod' || gutil.env.env === 'preprod' ? cleanCSS({processImport: false}) : gutil.noop();
}

var uglifyIfNeeded = function(alwaysUglify) {
    return alwaysUglify === true || gutil.env.env === 'prod' || gutil.env.env === 'preprod' ? uglify() : gutil.noop();
}

var errorHandler = function (err) {
    if (typeof err.file !== 'undefined') {
        console.log(err.file, err.line, err.messageOriginal);
    } else {
        console.log(err);
    }
    this.emit('end');
}

gulp.task('js', function () {
    return gulp.src(paths.src + 'js/**/*.*')
        .pipe(plumber({ errorHandler: errorHandler }))
        .pipe(uglifyIfNeeded())
        .pipe(concat('app.js'))
        .pipe(gulp.dest(paths.dest + 'js'));
});

gulp.task('fonts', function() {
    return gulp.src(paths.src + 'fonts/*')
        .pipe(gulp.dest(paths.dest + 'fonts'));
});

gulp.task('css', function () {
    return gulp.src(paths.src + 'scss/app.scss')
        .pipe(plumber({ errorHandler: errorHandler }))
        .pipe(sass())
        .pipe(autoprefixer({ browsers: ['last 2 versions'] }))
        .pipe(minifyIfNeeded(true))
        .pipe(concat('app.css'))
        .pipe(gulp.dest(paths.dest + 'css'));
});

gulp.task('css-fonts', function () {
    return gulp.src(paths.src + 'scss/fonts.scss')
        .pipe(plumber({ errorHandler: errorHandler }))
        .pipe(autoprefixer({ browsers: ['last 2 versions'] }))
        .pipe(minifyIfNeeded(true))
        .pipe(concat('fonts.css'))
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

gulp.task('image', function() {
    return gulp.src([paths.src + 'img/**/*.{jpg,jpeg,png}'])
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

exports.default = gulp.series(['css', 'js', 'image', 'webp', 'fonts', 'css-fonts'])


