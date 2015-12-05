angular.module('urn')
    .directive('revolutionSlider', function() {
        return {
            restrict: 'A',
            link: function(scope, element) {
                $(element).show().revolution({
                    dottedOverlay: 'none',
                    delay: 5000,
                    startwidth: 1920,
                    startheight: 650,

                    hideThumbs: 200,
                    thumbWidth: 200,
                    thumbHeight: 50,
                    thumbAmount: 2,

                    navigationType: 'thumb',
                    navigationArrows: 'solo',
                    navigationStyle: 'round',

                    touchenabled: 'on',
                    onHoverStop: 'on',

                    swipe_velocity: 0.7,
                    swipe_min_touches: 1,
                    swipe_max_touches: 1,
                    drag_block_vertical: false,

                    spinner: 'spinner0',
                    keyboardNavigation: 'off',

                    navigationHAlign: 'center',
                    navigationVAlign: 'bottom',
                    navigationHOffset: 0,
                    navigationVOffset: 20,

                    soloArrowLeftHalign: 'left',
                    soloArrowLeftValign: 'center',
                    soloArrowLeftHOffset: 20,
                    soloArrowLeftVOffset: 0,

                    soloArrowRightHalign: 'right',
                    soloArrowRightValign: 'center',
                    soloArrowRightHOffset: 20,
                    soloArrowRightVOffset: 0,

                    shadow: 0,
                    fullWidth: 'on',
                    fullScreen: 'off',

                    stopLoop: 'off',
                    stopAfterLoops: -1,
                    stopAtSlide: -1,

                    shuffle: 'off',

                    autoHeight: 'off',
                    forceFullWidth: 'on',
                    fullScreenAlignForce: 'off',
                    minFullScreenHeight: 0,
                    hideNavDelayOnMobile: 1500,

                    hideThumbsOnMobile: 'off',
                    hideBulletsOnMobile: 'off',
                    hideArrowsOnMobile: 'off',
                    hideThumbsUnderResolution: 0,

                    hideSliderAtLimit: 0,
                    hideCaptionAtLimit: 0,
                    hideAllCaptionAtLilmit: 0,
                    startWithSlide: 0,
                    fullScreenOffsetContainer: ''
                })
            }
        }
    })
    .directive('commonSlider', function() {
        return {
            restrict: 'A',
            scope: {
                itemCount : '='
            },
            link: function(scope, element) {
                $(element).owlCarousel({
                    items: parseInt(scope.itemCount), //10 items above 1000px browser width
                    itemsDesktop: [1024, 4], //5 items between 1024px and 901px
                    itemsDesktopSmall: [991, 3], // 3 items betweem 900px and 601px
                    itemsTablet: [600, 2], //2 items between 600 and 0;
                    itemsMobile: [320, 1],
                    navigation: true,
                    navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
                    slideSpeed: 500,
                    pagination: false
                });
            }
        }
    })
    .directive('offerSlider', function() {
        return {
            restrict: 'A',
            link: function(scope, element) {
                jQuery(document).ready(function () {
                   $(element).bxSlider({
                        mode: 'horizontal',
                        slideMargin: 3,
                        auto:true
                    });
                });
            }
        }
    });
