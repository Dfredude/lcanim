from manim import *

arr_scale = 1

class MaximumProductSubarray(Scene):
    def construct(self):
        arr = [6, -3, -10, 0, 2]
        # Display array elements and header
        title = Tex("Maximum Product Subarray").scale(1.5).to_edge(UP)
        arrStrs = []
        for i, num in enumerate(arr):
            arrStrs.append(str(num))
            arrStrs.append(', ')
        arrStrs.pop()
        arrTex = MathTex('[', *arrStrs, ']').scale(arr_scale)
        # Center the group of MathTex objects on the screen
        arrTex.move_to(ORIGIN)
        # Write the group of MathTex objects to the screen
        self.play(Write(arrTex), Write(title), run_time=0.5)
        arrTex.shift(LEFT * 3)
        
        # 2nd action: Traverse array and highlight elements while updating localmin, localmax and globalMax
        localmax, localMaxBounds = 1, [0, 0]
        localmin, localMinBounds = 1, [0, 0]
        globalMax = arr[0]
        # Display the initial values of localmin, localmax and globalMax
        localmaxTex1 = Tex("localmax: ").next_to(arrTex, RIGHT*4).scale(arr_scale).set_color(GREEN)
        localminTex1 = Tex("localmin: ").next_to(localmaxTex1, DOWN).scale(arr_scale).set_color(RED).align_to(localmaxTex1, LEFT)
        globalMaxTex1 = Tex("globalMax: ").next_to(localminTex1, DOWN).scale(arr_scale).align_to(localmaxTex1, LEFT)
        localmaxTex2 = MathTex("-\infty").next_to(localmaxTex1, RIGHT).scale(arr_scale).set_color(GREEN)
        localminTex2 = MathTex("-\infty").next_to(localminTex1, RIGHT).scale(arr_scale).set_color(RED)
        globalMaxTex2 = MathTex(" -\infty").next_to(globalMaxTex1, RIGHT).scale(arr_scale)
        texs = [localmaxTex1, localminTex1, globalMaxTex1, localmaxTex2, localminTex2, globalMaxTex2]
        # Write the initial values to the screen
        arrTex.shift(RIGHT * 3)
        self.play(*[Write(tex) for tex in texs], arrTex.animate.shift(LEFT * 3))
        localmaxRect = Dot(arrTex[1].get_center()).set_color(GREEN).scale(0.2)
        localminRect = Dot(arrTex[1].get_center()).set_color(RED).scale(0.2)
        for i in range(len(arr)):
            # Highlight the current element
            j =  i * 2 + 1
            highlight = arrTex[j].copy().set_color(YELLOW)
            self.play(Indicate(highlight))
            # Update localmin, localmax and globalMax
            print(localMaxBounds, localMinBounds)
            localMaxBounds.pop()
            localMinBounds.pop()
            possibilities = [(arr[i], [i, i]), 
                             (localmax * arr[i], localMaxBounds + [i]), 
                             (localmin * arr[i], localMinBounds + [i])]
            print(possibilities)
            possibilities.sort(key=lambda x: x[0], reverse=True)
            localmax = possibilities[0][0]
            localmin = possibilities[2][0]
            globalMax = max(globalMax, localmax)
            localMaxBounds = possibilities[0][1]
            localMinBounds = localMinBounds + [i]  if possibilities[2][0] == possibilities[1][0] else possibilities[2][1]
            # Generate surroinding rectangles for localmax and localmin subarrays
            updatedLocalmaxRect = SurroundingRectangle(arrTex[localMaxBounds[0] * 2 + 1: localMaxBounds[-1] * 2 + 2], buff = .2).set_color(GREEN)
            updatedLocalminRect = SurroundingRectangle(arrTex[localMinBounds[0] * 2 + 1: localMinBounds[-1] * 2 + 2], buff = .1).set_color(RED)
            # Display the surrounding rectangles & Display the updated values
            localmaxTexUpdated = MathTex(f"{localmax}").next_to(localmaxTex1, RIGHT).scale(arr_scale).set_color(GREEN)
            localminTexUpdated = MathTex(f"{localmin}").next_to(localminTex1, RIGHT).scale(arr_scale).set_color(RED)
            globalMaxTexUpdated = MathTex(f"{globalMax}").next_to(globalMaxTex1, RIGHT).scale(arr_scale)
            self.play(Transform(localmaxTex2, localmaxTexUpdated), Transform(localminTex2, localminTexUpdated),Transform(globalMaxTex2, globalMaxTexUpdated), 
                        Transform(localmaxRect, updatedLocalmaxRect), Transform(localminRect, updatedLocalminRect))
            # Pause for a moment to show the updated values``
            self.wait(0.5)
            # Remove the highlight
            self.play(FadeOut(highlight))
        self.wait(1)

