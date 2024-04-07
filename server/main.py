from sock import Sock

sock = Sock(host = "0.0.0.0", port = 16782, verbose = True)

sock.start(thread = False)