import xbmc
import xbmcaddon
import xbmcgui
from Utils import *
from TheMovieDB import *
from YouTube import *
import DialogActorInfo
homewindow = xbmcgui.Window(10000)

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__addonversion__ = __addon__.getAddonInfo('version')
__language__ = __addon__.getLocalizedString
__cwd__ = __addon__.getAddonInfo('path').decode("utf-8")


class DialogVideoInfo(xbmcgui.WindowXMLDialog):
    ACTION_PREVIOUS_MENU = [9, 92, 10]

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.id = kwargs.get('id')
        self.dbid = kwargs.get('dbid')
        name = kwargs.get('name')
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        if self.id:
            self.movie, self.actors = GetExtendedMovieInfo(self.id, self.dbid)
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory": "videodb://movies/actors/", "media": "files"}, "id": 1}')
            json_query = unicode(json_query, 'utf-8', errors='ignore')
            json_response = simplejson.loads(json_query)
            for db_actor in json_response["result"]["files"]:
                for movie_actor in self.actors:
                    if db_actor["label"] == movie_actor["name"]:
                        movie_actor.update({"dbid": db_actor["id"]})
                        json_query2 = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory": "videodb://movies/actors/%i/", "media": "files"}, "id": 1}' % db_actor["id"])
                        json_query2 = unicode(json_query2, 'utf-8', errors='ignore')
                        json_response2 = simplejson.loads(json_query2)
                        numfiles = len(json_response2["result"]["files"])
                        movie_actor.update({"moviecount": numfiles})
            self.youtube_vids = GetYoutubeSearchVideosV3(self.movie["Title"])
            passHomeDataToSkin(self.movie, "movie.")
         #   homewindow.setProperty("actor.TotalMovies", str(len(self.movie_roles)))
        else:
            Notify("No ID found")
        self.actor_listitems = CreateListItems(self.actors, 4)
        xbmc.executebuiltin("Dialog.Close(busydialog)")

    def onInit(self):
        xbmc.executebuiltin("SetFocus(8)")
        self.getControl(50).addItems(self.actor_listitems)
    #    self.getControl(150).addItems(tvshow_listitems)

    def onAction(self, action):
        if action in self.ACTION_PREVIOUS_MENU:
            self.close()

    def onClick(self, controlID):
        if controlID == 50:
            actorid = self.getControl(50).getSelectedItem().getProperty("id")
            dialog = DialogActorInfo.DialogActorInfo(u'script-%s-DialogInfo.xml' % __addonname__, __cwd__, id=actorid)
            self.close()
            dialog.doModal()

    def onFocus(self, controlID):
        pass