# -*- coding: utf-8 -*-
import sys
import e32
import appuifw as gui
import key_codes
sys.path.append("e:\\python")
from filesel import FileSel
import os

class Contents:
    def __init__(self, cbk, contents=u""):
        self.cbk = cbk
        self.cancel = False

        self.body = gui.Text( contents )
        self.body.focus = True

        self.refresh()
        
    def refresh(self):
        gui.app.exit_key_handler = self.close_app
        gui.app.title = u"New Post"

        gui.app.body = self.body
        gui.app.menu = [( u"Close", self.close_app ),\
                        ( u"Cancel", self.cancel_app )]          

    def cancel_app(self):
        self.cancel = True
        self.close_app()
        
    def close_app(self):
        if not self.cancel:
            self.cbk( self.body.get() )
        else:
            self.cbk( None )

    def run(self):
        pass
            
class NewPost:
    def __init__(self,
                 cbk,
                 title=u"",
                 contents=u"",
                 blog_categories = [u"Uncategorized"],                 
                 categories = [],
                 images = []):

        self.cbk = cbk
        self.title = title
        self.contents = contents
        self.blog_categories = blog_categories
        self.categories = categories
        self.images = images
        
        self.body = gui.Listbox( [ (u"",u"") ], self.update_value )
        self.cancel = False

        self.refresh()

    def refresh(self):
        gui.app.exit_key_handler = self.close_app
        gui.app.title = u"New Post"
        
        img = unicode(",".join(self.images))
        cat = unicode(",".join(self.categories))

        values = [ (u"Title", self.title ), \
                   (u"Contents", self.contents[:50]), \
                   (u"Categories", cat), \
                   (u"Images", img ) ]

        gui.app.body = self.body
        gui.app.body.set_list( values )
        gui.app.menu = [( u"Publish", self.close_app ),\
                        ( u"Cancel", self.cancel_app )]        
        
    def cancel_app(self):
        self.cancel = True
        self.close_app()
        
    def close_app(self):
        if not self.cancel:
            self.cbk( (self.title, self.contents, self.images, self.categories) )
        else:
            self.cbk( (None,None,None,None) )

    def update_value(self):
        idx = gui.app.body.current()
        if idx == 0:
            title = gui.query(u"Post title:","text", self.title)
            if title is not None:
                self.title = title
            self.refresh()
        elif idx == 1:
            def cbk( txt ):
                if txt is not None:
                    self.contents = txt
                self.refresh()
            self.dlg = Contents( cbk, self.contents )
            self.dlg.run()
        elif idx == 2:
            sel = gui.multi_selection_list( self.blog_categories, style='checkbox', search_field=1 )
            if len(sel) == 0:
                self.categories = [u"Uncategorized"]
            else:
                self.categories = [ self.blog_categories[idx] for idx in sel ]
            self.refresh()            
        elif idx == 3:
            ir = gui.popup_menu( [u"Insert", u"List", u"Remove"], u"Images")
            if ir is not None:
                if ir == 0:
                    sel = FileSel().run()
                    if sel is not None:
                        self.images.append( sel )
                elif ir == 1:
                    if len(self.images) > 0:
                        gui.selection_list(self.images, search_field=1)
                    else:
                        gui.note(u"No images selected","info")
                elif ir == 2:
                    if len(self.images) > 0:
                        item = gui.selection_list(self.images, search_field=1)
                        if item is not None:
                            self.images = self.images[:item] + self.images[item+1:]
                    else:
                        gui.note(u"No images selected","info")
            self.refresh()
        
    def run(self):
        pass

if __name__ == "__main__":

    cat = [u"Uncategorized", u"Cat A", u"Cat B", u"Cat C", u"Cat D", u"Cat E"]
    ep = NewPost(u"Title",u"Post contents",cat)
    print ep.run()