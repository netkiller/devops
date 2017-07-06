var gulp = require('gulp');
var argv = require('yargs').argv;
//var minifyHtml = require("gulp-minify-html");
var minifycss = require('gulp-clean-css');
//var minifycss = require("gulp-minify-css");
var spriter = require("gulp-spriter");
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var path = require("path");
var glob = require("glob");
var watch = require('gulp-watch');

var src = __dirname + "/" +  argv.src;
var dist = __dirname + "/" + argv.src;

gulp.task('minify-html', function () {
    gulp.src( src +'/*.html') // path to your files
    .pipe(minifyHtml())
    .pipe(gulp.dest( dist + '/'));
});

gulp.task('minify-css', function () {

	gulp.src([src + '/css/**/*.css', "!"+src + '/css/**/*.min.css'])
//	.pipe(concat("finally.css"))
	.pipe(rename({ suffix: '.min' }))
	.pipe(minifycss())
	.pipe(gulp.dest( dist + '/css'));

});

gulp.task('minify-js', function(){

	gulp.src([src + "/js/**/*.js", "!"+src + "/js/**/*.min.js"])
//	.pipe(concat("finally.js"))
        .pipe(rename({ suffix: '.min' }))
	.pipe(uglify())
	.pipe(gulp.dest( dist + '/js'))

});

gulp.task("spriter",["clean"],function(){
  return gulp.src( dist + "/css/finally.min.css")
         .pipe(spriter({
            sprite:"finally.png",
            slice: src + "/images",
            outpath: dist + "/images"
          }))
         .pipe(gulp.dest( dist + '/images'))
})


gulp.task('default',function() {
    gulp.start('minify-css','minify-js');
});

gulp.task('watch', function() {
    watch(src + "/css/**/*.css", function() {
        gulp.run('minify-css');
    });
    watch(src + "/js/**/*.js", function() {
        gulp.run('minify-js');
    });
});
