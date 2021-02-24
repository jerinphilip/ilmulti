Aligning Docs
=============

The following are snapshots of new pages with potential Translation Memories. There are many such documents available on the web.

* English: [Iruttu Kadai: Off to Taste The Best of Halwa!](https://www.nativeplanet.com/travel-guide/iruttu-kadai-the-taste-best-halwa-tirunelveli-002051.html) [wayback](https://web.archive.org/web/20201104190203/https://www.nativeplanet.com/travel-guide/iruttu-kadai-the-taste-best-halwa-tirunelveli-002051.html)
* Malayalam: [ഇരുട്ടുകട എന്ന വിചിത്രമായ ഹല്‍വക്കട!  ](https://malayalam.nativeplanet.com/travel-guide/iruttu-kadai-tirunelveli-000981.html) [wayback](https://web.archive.org/web/20160707175458/https://malayalam.nativeplanet.com/travel-guide/iruttu-kadai-tirunelveli-000981.html)

We will use this library to align the sentences from one of these to the other,
through the API to demonstrate the application, walking through the internals
of what is happening. For the purpose of this walkthrough, we will assume the
text blobs from these articles before processing are already available to us.

We will need to obtain sentences first to align these. For this, we use the
Punkt Segmenters provided in this library.




