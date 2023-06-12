# -*- coding: utf-8 -*-
# Copyright (c) 2023, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.
import unittest
from os import sep
from impl import AnnotationProcessor, MetadataProcessor, RelationalQueryProcessor
from impl import CollectionProcessor, TriplestoreQueryProcessor
from impl import GenericQueryProcessor
from pandas import DataFrame
from impl import IdentifiableEntity, EntityWithMetadata, Canvas, Collection, Image, Annotation, Manifest

# REMEMBER: before launching the tests, please run the Blazegraph instance!

class TestProjectBasic(unittest.TestCase):

    # The paths of the files used in the test should change depending on what you want to use
    # and the folder where they are. Instead, for the graph database, the URL to talk with
    # the SPARQL endpoint must be updated depending on how you launch it - currently, it is
    # specified the URL introduced during the course, which is the one used for a standard
    # launch of the database.
    annotations = "data" + sep + "annotations.csv"
    collection = "data" + sep + "collection-1.json"
    metadata = "data" + sep + "metadata.csv"
    relational = "." + sep + "relational.db"
    graph = "http://127.0.0.1:9999/blazegraph/sparql"
    
    def test_01_AnnotationProcessor(self):
        ann_dp = AnnotationProcessor()
        self.assertTrue(ann_dp.setDbPathOrUrl(self.relational))
        self.assertEqual(ann_dp.getDbPathOrUrl(), self.relational)
        self.assertTrue(ann_dp.uploadData(self.annotations))

    def test_02_MetadataProcessor(self):
        met_dp = MetadataProcessor()
        self.assertTrue(met_dp.setDbPathOrUrl(self.relational))
        self.assertEqual(met_dp.getDbPathOrUrl(), self.relational)
        self.assertTrue(met_dp.uploadData(self.metadata))

    def test_03_CollectionProcessor(self):
        col_dp = CollectionProcessor()
        self.assertTrue(col_dp.setDbPathOrUrl(self.graph))
        self.assertEqual(col_dp.getDbPathOrUrl(), self.graph)
        self.assertTrue(col_dp.uploadData(self.collection))

    def test_04_RelationalQueryProcessor(self):
        rel_qp = RelationalQueryProcessor()
        self.assertTrue(rel_qp.setDbPathOrUrl(self.relational))

        self.assertIsInstance(rel_qp.getAllAnnotations(), DataFrame)
        self.assertIsInstance(rel_qp.getAllImages(), DataFrame)
        self.assertIsInstance(rel_qp.getAnnotationsWithBody("just_a_test"), DataFrame)
        self.assertIsInstance(rel_qp.getAnnotationsWithBodyAndTarget("just_a_test", "another_test"), DataFrame)
        self.assertIsInstance(rel_qp.getAnnotationsWithTarget("just_a_test"), DataFrame)
        self.assertIsInstance(rel_qp.getEntityById("just_a_test"), DataFrame)
        self.assertIsInstance(rel_qp.getEntitiesWithCreator("just_a_test"), DataFrame)
        self.assertIsInstance(rel_qp.getEntitiesWithTitle("just_a_test"), DataFrame)

    def test_05_TriplestoreQueryProcessor(self):
        grp_qp = TriplestoreQueryProcessor()
        self.assertTrue(grp_qp.setDbPathOrUrl(self.graph))

        self.assertIsInstance(grp_qp.getAllCanvases(), DataFrame)
        self.assertIsInstance(grp_qp.getAllCollections(), DataFrame)
        self.assertIsInstance(grp_qp.getAllManifests(), DataFrame)
        self.assertIsInstance(grp_qp.getCanvasesInCollection("just_a_test"), DataFrame)
        self.assertIsInstance(grp_qp.getCanvasesInManifest("just_a_test"), DataFrame)
        self.assertIsInstance(grp_qp.getEntityById("just_a_test"), DataFrame)
        self.assertIsInstance(grp_qp.getEntitiesWithLabel("just_a_test"), DataFrame)
        self.assertIsInstance(grp_qp.getManifestsInCollection("just_a_test"), DataFrame)

    def test_06_GenericQueryProcessor(self):
        rel_qp = RelationalQueryProcessor()
        rel_qp.setDbPathOrUrl(self.relational)
        grp_qp = TriplestoreQueryProcessor()
        grp_qp.setDbPathOrUrl(self.graph)

        generic = GenericQueryProcessor()
        self.assertIsInstance(generic.cleanQueryProcessors(), bool)
        self.assertTrue(generic.addQueryProcessor(rel_qp))
        self.assertTrue(generic.addQueryProcessor(grp_qp))
        
        self.assertIsInstance(generic.getAllAnnotations(), list)
        ann_1 = generic.getAllAnnotations()
        self.assertIsInstance(ann_1, list)
        for a in ann_1:
            self.assertIsInstance(a, Annotation)

        self.assertIsInstance(generic.getAllCanvas(), list)
        can_1 = generic.getAllCanvas()
        self.assertIsInstance(can_1, list)
        for a in can_1:
            self.assertIsInstance(a, Canvas)

        self.assertIsInstance(generic.getAllCollections(), list)
        col_1 = generic.getAllCollections()
        self.assertIsInstance(col_1, list)
        for a in col_1:
            self.assertIsInstance(a, Collection)

        self.assertIsInstance(generic.getAllImages(), list)
        ima_1 = generic.getAllImages()
        self.assertIsInstance(ima_1, list)
        for a in ima_1:
            self.assertIsInstance(a, Image)

        self.assertIsInstance(generic.getAllManifests(), list)
        man_1 = generic.getAllManifests()
        self.assertIsInstance(man_1, list)
        for a in man_1:
            self.assertIsInstance(a, Manifest)
        
        self.assertIsInstance(generic.getAnnotationsToCanvas("just_a_test"), list)
        ann_2 = generic.getAnnotationsToCanvas("https://dl.ficlit.unibo.it/iiif/2/28429/canvas/p1")
        self.assertIsInstance(ann_2, list)
        for a in ann_2:
            self.assertIsInstance(a, Annotation)

        self.assertIsInstance(generic.getAnnotationsToCollection("just_a_test"), list)
        ann_3 = generic.getAnnotationsToCollection("https://dl.ficlit.unibo.it/iiif/28429/collection")
        self.assertIsInstance(ann_3, list)
        for a in ann_3:
            self.assertIsInstance(a, Annotation)

        self.assertIsInstance(generic.getAnnotationsToManifest("just_a_test"), list)
        ann_4 = generic.getAnnotationsToManifest("https://dl.ficlit.unibo.it/iiif/2/28429/manifest")
        self.assertIsInstance(ann_4, list)
        for a in ann_4:
            self.assertIsInstance(a, Annotation)

        self.assertIsInstance(generic.getAnnotationsWithBody("just_a_test"), list)
        ann_5 = generic.getAnnotationsWithBody("https://dl.ficlit.unibo.it/iiif/2/45499/full/699,800/0/default.jpg")
        self.assertIsInstance(ann_5, list)
        for a in ann_5:
            self.assertIsInstance(a, Annotation)

        self.assertIsInstance(generic.getAnnotationsWithBodyAndTarget("just_a_test", "just_a_test"), list)
        ann_6 = generic.getAnnotationsWithBodyAndTarget("https://dl.ficlit.unibo.it/iiif/2/45499/full/699,800/0/default.jpg", "https://dl.ficlit.unibo.it/iiif/2/28429/canvas/p3")
        self.assertIsInstance(ann_6, list)
        for a in ann_6:
            self.assertIsInstance(a, Annotation)

        self.assertIsInstance(generic.getAnnotationsWithTarget("just_a_test"), list)
        ann_7 = generic.getAnnotationsWithTarget("https://dl.ficlit.unibo.it/iiif/2/28429/canvas/p3")
        self.assertIsInstance(ann_7, list)
        for a in ann_7:
            self.assertIsInstance(a, Annotation)

        self.assertIsInstance(generic.getCanvasesInCollection("just_a_test"), list)
        can_2 = generic.getCanvasesInCollection("https://dl.ficlit.unibo.it/iiif/28429/collection")
        self.assertIsInstance(can_2, list)
        for a in can_2:
            self.assertIsInstance(a, Canvas)

        self.assertIsInstance(generic.getCanvasesInManifest("just_a_test"), list)
        can_2 = generic.getCanvasesInManifest("https://dl.ficlit.unibo.it/iiif/2/28429/manifest")
        self.assertIsInstance(can_2, list)
        for a in can_2:
            self.assertIsInstance(a, Canvas)

        # It must return None in case the entity does not exist
        self.assertEqual(generic.getEntityById("just_a_test"), None)
        
        self.assertIsInstance(generic.getEntitiesWithCreator("just_a_test"), list)
        ent_1 = generic.getEntitiesWithCreator("Alighieri, Dante")
        self.assertIsInstance(ent_1, list)
        for a in ent_1:
            self.assertIsInstance(a, EntityWithMetadata)

        self.assertIsInstance(generic.getEntitiesWithLabel("just_a_test"), list)
        ent_2 = generic.getEntitiesWithLabel("Il Canzoniere")
        self.assertIsInstance(ent_2, list)
        for a in ent_2:
            self.assertIsInstance(a, EntityWithMetadata)

        self.assertIsInstance(generic.getEntitiesWithTitle("just_a_test"), list) # : list[EntityWithMetadata]
        ent_3 = generic.getEntitiesWithTitle("Dante Alighieri: Opere")
        self.assertIsInstance(ent_3, list)
        for a in ent_3:
            self.assertIsInstance(a, EntityWithMetadata)

        self.assertIsInstance(generic.getImagesAnnotatingCanvas("just_a_test"), list)
        ima_2 = generic.getImagesAnnotatingCanvas("https://dl.ficlit.unibo.it/iiif/2/28429/canvas/p7")
        self.assertIsInstance(ima_2, list)
        for a in ima_2:
            self.assertIsInstance(a, Image)

        self.assertIsInstance(generic.getManifestsInCollection("just_a_test"), list)
        man_2 = generic.getManifestsInCollection("https://dl.ficlit.unibo.it/iiif/28429/collection")
        self.assertIsInstance(man_2, list)
        for a in man_2:
            self.assertIsInstance(a, Manifest)
