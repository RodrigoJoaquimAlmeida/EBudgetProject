// https://www.kommo.com/developers/content/integrations/development-example/

// loadPreloadedData: function () {
//     return new Promise(_.bind(function (resolve, reject) {
//         // Let's make a request to a remote server
//         self.crm_post(
//             'http://my.sdk.api.com',
//             {},
//             function (msg1) {
//                 // Let's bring the elements to the desired format and resolve
//                 resolve(msg);
//             },
//             'json'
//         );
//     }), this);
// }

// loadElements: function (type, id) {
//     return new Promise(_.bind(function (resolve, reject) {
//         // Let's make a request to a remote server
//         self.crm_post(
//             'http://my.sdk.api.com',
//             {},
//             function (msg2) {
//                 // Let's bring the elements to the desired format and resolve
//                 resolve(msg);
//             },
//             'json'
//         );
//     }), this);
// }

// linkCard: function (links) {
//     return new Promise(_.bind(function (resolve, reject) {
//         // Let's make a request to a remote server
//         self.crm_post(
//             'http://my.sdk.api.com/sdk_back/link.php',
//             links,
//             function () {
//             // We do not process errors that could occur on your side, in this block you can execute
// Your code
//             },
//             'json'
//         );


//         resolve();
//     }), this);
// }