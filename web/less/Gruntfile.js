module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        less: {
            lessc: {
                files: [
                    {
                        expand: true,
                        cwd: './',
                        src: ['./*.less', '!./util/*.less'],
                        dest: '../css/',
                        ext: '.css'
                    }
                ]
            }
        },
        watch: {
            lesss: {
                files: ['./*.less', './*/*.less'],
                tasks: ['lessc']
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('lessc', ['less', 'watch']);
};
