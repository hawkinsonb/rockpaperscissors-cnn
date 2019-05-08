//
//  Generated file. Do not edit.
//

#import "GeneratedPluginRegistrant.h"
#import <camera/CameraPlugin.h>
#import <screen/ScreenPlugin.h>
#import <tflite/TflitePlugin.h>

@implementation GeneratedPluginRegistrant

+ (void)registerWithRegistry:(NSObject<FlutterPluginRegistry>*)registry {
  [CameraPlugin registerWithRegistrar:[registry registrarForPlugin:@"CameraPlugin"]];
  [ScreenPlugin registerWithRegistrar:[registry registrarForPlugin:@"ScreenPlugin"]];
  [TflitePlugin registerWithRegistrar:[registry registrarForPlugin:@"TflitePlugin"]];
}

@end
