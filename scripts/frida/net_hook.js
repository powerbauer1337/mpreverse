// Frida script to hook network operations in MarsPro app
// This script captures HTTP/HTTPS API calls for reverse engineering

console.log("[+] MarsPro Network Hook Loaded");

// Hook HTTP/HTTPS operations
Java.perform(function() {
    console.log("[+] Starting network hooks...");
    
    // Hook HttpURLConnection
    try {
        var HttpURLConnection = Java.use("java.net.HttpURLConnection");
        
        // Hook setRequestMethod
        HttpURLConnection.setRequestMethod.implementation = function(method) {
            console.log("[NET] HTTP Method: " + method);
            console.log("[NET] URL: " + this.getURL().toString());
            return this.setRequestMethod(method);
        };
        
        // Hook setRequestProperty
        HttpURLConnection.setRequestProperty.implementation = function(key, value) {
            console.log("[NET] Header: " + key + " = " + value);
            return this.setRequestProperty(key, value);
        };
        
        // Hook getInputStream
        HttpURLConnection.getInputStream.implementation = function() {
            console.log("[NET] Reading response from: " + this.getURL().toString());
            console.log("[NET] Response Code: " + this.getResponseCode());
            return this.getInputStream();
        };
        
        // Hook getOutputStream
        HttpURLConnection.getOutputStream.implementation = function() {
            console.log("[NET] Writing request to: " + this.getURL().toString());
            return this.getOutputStream();
        };
        
        console.log("[+] HttpURLConnection hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook HttpURLConnection: " + e);
    }
    
    // Hook OkHttp (if used)
    try {
        var OkHttpClient = Java.use("okhttp3.OkHttpClient");
        
        OkHttpClient.newCall.implementation = function(request) {
            console.log("[NET] OkHttp Request:");
            console.log("  URL: " + request.url().toString());
            console.log("  Method: " + request.method());
            console.log("  Headers: " + request.headers().toString());
            return this.newCall(request);
        };
        
        console.log("[+] OkHttpClient hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook OkHttpClient: " + e);
    }
    
    // Hook URL creation
    try {
        var URL = Java.use("java.net.URL");
        
        URL.$init.overload('java.lang.String').implementation = function(url) {
            console.log("[NET] URL Created: " + url);
            return this.$init(url);
        };
        
        console.log("[+] URL hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook URL: " + e);
    }
    
    // Hook JSON operations
    try {
        var JSONObject = Java.use("org.json.JSONObject");
        
        JSONObject.$init.overload('java.lang.String').implementation = function(json) {
            console.log("[NET] JSON Object Created:");
            console.log("  Content: " + json);
            return this.$init(json);
        };
        
        JSONObject.toString.implementation = function() {
            var result = this.toString();
            console.log("[NET] JSON Object Serialized:");
            console.log("  Content: " + result);
            return result;
        };
        
        console.log("[+] JSONObject hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook JSONObject: " + e);
    }
    
    // Hook Firebase operations
    try {
        var FirebaseAuth = Java.use("com.google.firebase.auth.FirebaseAuth");
        
        FirebaseAuth.signInWithEmailAndPassword.implementation = function(email, password) {
            console.log("[NET] Firebase Auth Sign In:");
            console.log("  Email: " + email);
            console.log("  Password: [HIDDEN]");
            return this.signInWithEmailAndPassword(email, password);
        };
        
        FirebaseAuth.getCurrentUser.implementation = function() {
            var user = this.getCurrentUser();
            if (user) {
                console.log("[NET] Firebase Current User:");
                console.log("  UID: " + user.getUid());
                console.log("  Email: " + user.getEmail());
            }
            return user;
        };
        
        console.log("[+] FirebaseAuth hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook FirebaseAuth: " + e);
    }
    
    // Hook SSL/TLS operations
    try {
        var HttpsURLConnection = Java.use("javax.net.ssl.HttpsURLConnection");
        
        HttpsURLConnection.setSSLSocketFactory.implementation = function(factory) {
            console.log("[NET] SSL Socket Factory Set");
            return this.setSSLSocketFactory(factory);
        };
        
        console.log("[+] HttpsURLConnection hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook HttpsURLConnection: " + e);
    }
    
    // Hook InputStream/OutputStream for request/response body capture
    try {
        var ByteArrayOutputStream = Java.use("java.io.ByteArrayOutputStream");
        
        ByteArrayOutputStream.toByteArray.implementation = function() {
            var result = this.toByteArray();
            try {
                var content = Java.use("java.lang.String").$new(result, "UTF-8");
                console.log("[NET] Request/Response Body:");
                console.log("  Content: " + content);
            } catch (e) {
                console.log("[NET] Binary content (length: " + result.length + ")");
            }
            return result;
        };
        
        console.log("[+] ByteArrayOutputStream hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook ByteArrayOutputStream: " + e);
    }
    
    // Hook AsyncTask for background network operations
    try {
        var AsyncTask = Java.use("android.os.AsyncTask");
        
        AsyncTask.doInBackground.implementation = function(params) {
            console.log("[NET] AsyncTask Background Operation Started");
            return this.doInBackground(params);
        };
        
        console.log("[+] AsyncTask hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook AsyncTask: " + e);
    }
    
    // Hook Thread operations for network threads
    try {
        var Thread = Java.use("java.lang.Thread");
        
        Thread.start.implementation = function() {
            console.log("[NET] Thread Started: " + this.getName());
            return this.start();
        };
        
        console.log("[+] Thread hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook Thread: " + e);
    }
});

// Hook Flutter-specific network operations
Java.perform(function() {
    try {
        // Hook Flutter HTTP client if available
        var FlutterHttpClient = Java.use("io.flutter.plugin.common.MethodChannel");
        
        FlutterHttpClient.invokeMethod.implementation = function(method, arguments) {
            console.log("[NET] Flutter Method Channel:");
            console.log("  Method: " + method);
            console.log("  Arguments: " + arguments);
            return this.invokeMethod(method, arguments);
        };
        
        console.log("[+] Flutter MethodChannel hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook Flutter MethodChannel: " + e);
    }
});

// Hook DNS resolution
Java.perform(function() {
    try {
        var InetAddress = Java.use("java.net.InetAddress");
        
        InetAddress.getByName.implementation = function(host) {
            console.log("[NET] DNS Resolution: " + host);
            return this.getByName(host);
        };
        
        console.log("[+] InetAddress hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook InetAddress: " + e);
    }
});

console.log("[+] Network hooks installation complete");
console.log("[+] Monitor the output for API calls and network communication");
console.log("[+] Look for patterns in URLs, headers, and request/response bodies"); 