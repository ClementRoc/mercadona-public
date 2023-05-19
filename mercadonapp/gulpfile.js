'use strict';

// Define all the variables
// Fetch the package.json extensions
var gulp = require('gulp'),
    sass = require('gulp-sass')(require('sass')),
    rename = require('gulp-rename'),
    plumber = require('gulp-plumber'),
    babel = require('gulp-babel'),
    gutil = require('gulp-util'),
    cleanCSS = require('gulp-clean-css'),
    addSrc = require('gulp-add-src'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat'),
    autoprefixer = require('gulp-autoprefixer'),
    webp = require('gulp-webp');


// Define the paths for the project
var paths = {
    src: './assets/',
    dest: './static/',
    imgDest: './static/img/',
    npm: 'node_modules/'
};

// Minify (compress) the CSS files
var minifyIfNeeded = function (alwaysMinify) {
    return alwaysMinify === true ? cleanCSS({processImport: false}) : gutil.noop();
}

// Uglify (Parse) the JS files
var uglifyIfNeeded = function(alwaysUglify) {
    return alwaysUglify === true ? uglify() : gutil.noop();
}

// Simple error handler
var errorHandler = function (err) {
    if (typeof err.file !== 'undefined') {
        console.log(err.file, err.line, err.messageOriginal);
    } else {
        console.log(err);
    }
    this.emit('end');
}

// Gulp task for the JS files.
// Get all the .js files in Assets folder (private) and compress it in a single .js file
// put on the Static folder (public)
gulp.task('js', function () {
    return gulp.src(paths.src + 'js/**/*.*')
        .pipe(plumber({ errorHandler: errorHandler }))
        .pipe(babel({ presets: ['es2015'] }))
        .pipe(uglifyIfNeeded())
        .pipe(addSrc.prepend([
            paths.npm + 'jquery/dist/jquery.min.js'
        ]))
        .pipe(concat('app.js'))
        .pipe(gulp.dest(paths.dest + 'js'));
});

// Gulp task for the fonts
// Get all the fonts files in Assets folder (private) and put in on the Static folder (public)
gulp.task('fonts', function() {
    return gulp.src(paths.src + 'fonts/*')
        .pipe(gulp.dest(paths.dest + 'fonts'));
});

// Gulp task for the CSS files.
// Get all the .scss files in Assets folder (private) and compress it in a single .css file
// put on the Static folder (public)
gulp.task('css', function () {
    return gulp.src(paths.src + 'scss/app.scss')
        .pipe(plumber({ errorHandler: errorHandler }))
        .pipe(sass())
        .pipe(autoprefixer({ browsers: ['last 2 versions'] }))
        .pipe(minifyIfNeeded(true))
        .pipe(concat('app.css'))
        .pipe(gulp.dest(paths.dest + 'css'));
});

// Gulp task for the CSS-fonts files.
// Get all the .scss files in Assets folder (private) and compress it in a single .css file
// put on the Static folder (public)
gulp.task('css-fonts', function () {
    return gulp.src(paths.src + 'scss/fonts.scss')
        .pipe(plumber({ errorHandler: errorHandler }))
        .pipe(autoprefixer({ browsers: ['last 2 versions'] }))
        .pipe(minifyIfNeeded(true))
        .pipe(concat('fonts.css'))
        .pipe(gulp.dest(paths.dest + 'css'));
});

// gulp.task('webp', function() {
//     return gulp.src([paths.src + 'img/**/*.{jpg,jpeg,png}'])
//         .pipe(rename({
//             extname: '.webp',
//         }))
//         .pipe(webp({ quality: 80 }))
//         .pipe(gulp.dest(paths.imgDest));
// });

// Gulp task for the images
// Get all the images files in Assets folder (private) and put in on the Static folder (public)
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

// Define the tasks when you call the gulp by default
exports.default = gulp.series(['css', 'js', 'image', 'fonts', 'css-fonts'])


